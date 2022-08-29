
from collections import deque
import math


# class for control commands within loop
class CommandError(Exception):
    def __init__(self, message):
        self.message = message


assignments = {}


def get_precedence(char):
    if char == '^':
        return 3
    if char == '*' or char == '/':
        return 2
    if char == '+' or char == '-':
        return 1
    return -1


def is_assignment(string):
    tokens = string.split('=')
    if len(tokens) == 2:
        key = tokens[0].strip()
        if not key.isalpha():
            raise TypeError('Invalid identifier')
        valstr = tokens[1].strip()
        if not valstr.isalpha():
            try:
                value = int(valstr)
            except ValueError:
                raise ValueError('Invalid assignment')
        else:
            value = assignments.get(valstr)
            if value is None:
                raise NameError('Unknown variable')
        assignments[key] = value
        return True
    elif len(tokens) > 2:
        raise ValueError('Invalid assignment')
    return False


def is_command(string):
    if string[0] == "/":
        if line == "/help":
            print('The program calculates the sum of numbers. It supports multiplication, integer division, '
                  'parentheses, addition, and both unary and binary minus operators.')
        elif line == "/exit":
            raise CommandError('Exit command')
        else:
            raise CommandError('Unknown command')
        return True
    return False


def is_minus(token):
    return token[0] == '-' and len(token) % 2 == 1


def to_infix(string):
    infix = list()
    temp = ""
    prev = None
    minus = 0
    for char in string:
        if char.isalpha() or char.isdigit():
            if prev is not None:
                if prev == '-':
                    if minus % 2 == 0:
                        prev = '+'
                    minus = 0
                infix.append(prev)
                prev = None
            temp += char
        else:
            if len(temp) > 0:
                infix.append(temp)
                temp = ""
            if prev is not None and prev == ')':
                infix.append(prev)
                prev = None
            if char == '(':
                if prev is not None:
                    if prev == '-':
                        if minus % 2 == 0:
                            prev = '+'
                        minus = 0
                    infix.append(prev)
                prev = char
            if char == ')' or char == '*' or char == '/':
                if prev is not None:
                    raise ValueError('Invalid expression')
                prev = char
            if char == '+' or char == '-':
                if prev is not None and prev != char:
                    raise ValueError('Invalid expression')
                if char == '-':
                    minus += 1
                prev = char
    if len(temp) > 0:
        infix.append(temp)
    if prev is not None:
        if prev == '-' and minus % 2 == 0:
            prev = '+'
        infix.append(prev)
    return infix


def to_postfix(string):
    infix = to_infix(string)
    postfix = deque()
    stack = deque()
    for i in infix:
        if i.isalpha() or i.isdigit():
            postfix.append(i)
        else:
            if len(stack) == 0 or peek_stack(stack) == '(':
                stack.append(i)
            elif i == '(':
                stack.append(i)
            elif i == ')':
                while len(stack) > 0 and peek_stack(stack) != '(':
                    postfix.append(stack.pop())
                if len(stack) == 0:
                    raise ValueError('Invalid expression')
                stack.pop()
            elif get_precedence(peek_stack(stack)) < get_precedence(i):
                stack.append(i)
            elif get_precedence(peek_stack(stack)) >= get_precedence(i):
                while len(stack) > 0 and peek_stack(stack) != '(' and \
                        get_precedence(peek_stack(stack)) >= get_precedence(i):
                    postfix.append(stack.pop())
                stack.append(i)
    while len(stack) > 0:
        if peek_stack(stack) == '(':
            raise ValueError('Invalid expression')
        postfix.append(stack.pop())
    return postfix


def peek_stack(stack):
    return stack[len(stack) - 1]


def calculate_sum(string):
    total = deque()
    postfix = to_postfix(string)
    for p in postfix:
        if p.isdigit():
            total.append(int(p))
        elif p.isalpha():
            num = assignments.get(p)
            if num is None:
                raise NameError('Unknown variable')
            total.append(num)
        else:
            num1 = total.pop()
            try:
                num2 = total.pop()
            except IndexError:
                num2 = 0
            if p[0] == '*':
                num3 = num2 * num1
            elif p[0] == '/':
                num3 = num2 / num1
            elif p[0] == '+':
                num3 = num2 + num1
            elif p[0] == '-':
                num3 = num2 - num1
            else:
                num3 = math.pow(num1, num2)
            total.append(num3)
    print(int(total.pop()))


while True:
    line = input()
    try:
        if len(line) == 0 or is_command(line) or is_assignment(line):
            continue
        calculate_sum(line)
    except CommandError as ce:
        if ce.message == "Exit command":
            break
        print(ce.message)
    except NameError as ne:
        print(ne)
    except TypeError as te:
        print(te)
    except ValueError as ve:
        print(ve)
print('Bye!')
