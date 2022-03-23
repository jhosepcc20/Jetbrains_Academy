import re
from collections import deque


def check(expression, table):
    sings = [i.strip() for i in re.split(r"\w ?", '+' + expression) if i]
    digits = [i.strip() for i in re.split("[-+()*/] ?", expression) if i]
    expression = expression.replace('(', "( ").replace(')', " )").replace('+', " + ").replace('-', " - ").\
        replace('*', " * ").replace('/', " / ")
    expression = [i if i.lstrip("+-") else '-' if i.count('-') % 2 else '+' for i in expression.split()]
    expression = [table.get(i, "None") if i.isalpha() else i for i in expression]
    assert all(map(lambda x: x.isdigit() or x.isalpha(), digits)), "Invalid expression"
    assert not any(map(lambda x: len(x.strip("() ")) > 1 and x.strip("() ")[0] in "*/^", sings)), "Invalid expression"
    assert "None" not in expression, "Unknown variable"

    return expression


def infix_to_postfix(infix: list[str]) -> list:
    stack = deque()
    ops = {'-': 0, '+': 0, '*': 1, '/': 2, '^': 3}
    result = []

    for i in infix:
        if i.lstrip("+-").isdigit():
            result.append(i)
        elif i == '(':
            stack.append(i)
        elif i == ')':
            while stack:
                if stack[-1] == '(':
                    stack.pop()
                    break
                result.append(stack.pop())
            else:
                raise Exception("Invalid expression")

        else:
            if not stack or stack[-1] == '(':
                stack.append(i)
            elif ops[i] > ops[stack[-1]]:
                stack.append(i)
            else:
                while stack:
                    if ops[i] > ops.get(stack[-1], 4) or stack[-1] == '(':
                        break
                    result.append(stack.pop())
                stack.append(i)

    assert '(' not in stack, "Invalid expression"
    while stack:
        result.append(stack.pop())

    return result


def calculate(postfix: list[str]):
    stack = deque()

    for i in postfix:
        if i.lstrip("+-").isdigit():
            stack.append(i)
        else:
            b = int(stack.pop())
            a = int(stack.pop())

            if i == '-':
                stack.append(a - b)
            elif i == '+':
                stack.append(a + b)
            elif i == '*':
                stack.append(a * b)
            elif i == '^':
                stack.append(a ** b)
            else:
                stack.append(a / b)

    return stack.pop()


def main():
    table = dict()
    while True:
        command = input()
        if command:
            if command.startswith('/'):
                if command == "/exit":
                    print("Bye!")
                    break
                elif command == "/help":
                    print("The program calculates the sum and subtraction of numbers")
                else:
                    print("Unknown command")
            elif '=' in command:
                command = command.replace(' ', '')
                key, value = command.split('=', maxsplit=1)
                if not key.isalpha():
                    print("Invalid identifier")
                else:
                    if value.isdigit():
                        table[key] = value
                    elif value.isalpha():
                        if value in table.keys():
                            table[key] = table[value]
                        else:
                            print("Unknown variable")
                    else:
                        print("Invalid assignment")
            else:
                try:
                    print(calculate(infix_to_postfix(check(command, table))))
                except AssertionError as err:
                    print(err)
                except Exception as err:
                    print(err)


if __name__ == "__main__":
    main()
