import sys
import os
import re
import ast


def check_lon(line: str) -> bool:
    return len(line) > 79


def check_ind(line: str) -> bool:
    return (len(line) - len(line.lstrip())) % 4 != 0


def check_sem(line: str) -> bool:
    return line.split('#')[0].rstrip().endswith(';')


def check_spa(line: str) -> bool:
    if '#' in line and not line.strip().startswith('#'):
        lin_code = line[:line.find('#')]
        return len(lin_code) - len(lin_code.rstrip()) < 2
    return False


def check_todo(line: str) -> bool:
    if '#' in line:
        lin_com = line[line.find('#') + 1:]
        return any(map(lambda x: x.lower() == "todo", lin_com.split()))
    return False


def check_bla(count: int) -> bool:
    return count > 2


def main():
    arg = sys.argv[1]
    if os.path.isdir(arg):
        files_py = list(filter(lambda x: x.split('.')[-1] == "py", os.listdir(arg)))
        files_dir = list(map(lambda x: os.path.join(arg, x), files_py))
    else:
        files_dir = [arg]
    for file in files_dir:
        with open(file, 'r') as f:
            line_codes = list(map(lambda x: x.strip('\n'), f.readlines()))
            f.seek(0)
            tree = ast.parse(f.read())
        analyser = Analyzer(file, line_codes)
        analyser.visit(tree)
        analyser.check_code()


class Analyzer(ast.NodeVisitor):
    def __init__(self, file: str, lines: list[str]):
        self.file = file
        self.lines = lines
        self.errors = []

    def visit_FunctionDef(self, node):
        name = node.name
        self.space(name, node.lineno)
        if not re.fullmatch(r"[a-z\d_]+", name):
            self.errors.append((node.lineno, f"S009 Function {name} should use snake_case"))
        args = [arg.arg for arg in node.args.args if not re.fullmatch(r"[a-z\d_]+", arg.arg)]
        for arg in args:
            self.errors.append((node.lineno, f"S010 Argument name '{arg}' should use snake_case"))
        defaults = [isinstance(arg, (ast.List, ast.Dict, ast.Set)) for arg in node.args.defaults]
        if any(defaults):
            self.errors.append((node.lineno, f"S012 Default argument values is mutable"))
        for n in ast.walk(node):
            if isinstance(n, ast.Assign):
                if isinstance(n.targets[0], ast.Name):
                    var = n.targets[0].id
                else:
                    var = n.targets[0].attr
                if not re.fullmatch(r"[a-z\d_]+", var):
                    self.errors.append((n.lineno, f"S011 Variable '{var}' in function should be snake_case"))
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        name = node.name
        self.space(name, node.lineno)
        if not re.fullmatch(r"[A-Z][a-zA-Z\d]+", name):
            self.errors.append((node.lineno, f"S008 Class name '{name}' should be CamelCase"))
        self.generic_visit(node)

    def space(self, name, idx):
        names = self.lines[idx - 1]
        line = names.strip()
        lin_cod = line.split(name)[0]
        if lin_cod.count(' ') > 1:
            self.errors.append((idx, f"S007 Too many spaces after '{lin_cod.strip()}'"))

    def check_code(self):
        error_names = ["Too long", "Indentation is not a multiple of four", "Unnecessary semicolon",
                       "At least two spaces required before inline comments", "TODO found",
                       "More than two blank lines used before this line"]
        list_check = [check_lon, check_ind, check_sem, check_spa, check_todo, check_bla]
        count = 0
        for v, line in enumerate(self.lines):
            if not line:
                count += 1
            else:
                for err, fun in enumerate(list_check):
                    arg = count if err == 5 else line
                    if fun(arg):
                        self.errors.append((v + 1, f"S00{err + 1} {error_names[err]}"))
                count = 0
        self.errors.sort()
        for v, i in self.errors:
            print(f"{self.file}: Line {v}: {i}")


if __name__ == "__main__":
    main()
