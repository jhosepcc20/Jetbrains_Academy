import re
from collections import deque


def check(expression, table):
    expression = expression.replace(' ', '')
    expression = expression.replace('(', " (").replace(')', ") ")
    sings = [i.strip() for i in re.split(r"[\w ] ?", '+' + expression) if i]
    sings = [i if i[0] not in "+-" else '-' if i.count('-') % 2 else '+' for i in sings]
    digits = [i.strip() for i in re.split("[-+()*/^] ?", expression) if i]

    assert all(map(lambda x: x.isdigit() or x.isalpha(), digits)), "Invalid expression"
    assert not any(map(lambda x: x[0] in "*/^" and len(x) > 1, sings)), "Invalid expression"
    digits = [table.get(i, "None") if i.isalpha() else i for i in digits]
    assert "None" not in digits, "Unknown variable"
    result = [sings.pop(0) + digits.pop(0)]
    count = 0
    for i in digits:
        aux = sings.pop(0)
        result.append(aux)
        if aux == ')':
            count -= 1
            while sings[0] == ')':
                count -= 1
                result.append(sings.pop(0))
            result.append(sings.pop(0))
        elif sings:
            while sings[0] == '(':
                count += 1
                result.append(sings.pop(0))
                if not sings:
                    break
        result.append(i)
    while count and sings:
        count -= 1
        result.append(sings.pop(0))
    assert not sings, "Invalid expression"
    return result


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

    return int(stack.pop())


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
