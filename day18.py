import math
import re

ADDITION = re.compile('[0-9()+*]*?(\d+\+\d+)[0-9()+*]*')

def evaluate_left_to_right(expr):
    expr = list(expr.replace(' ', ''))[::-1] if isinstance(expr, str) else expr
    total = None
    method = None

    while expr:
        cur = expr.pop()
        if cur == '+':
            method = sum
        elif cur == '*':
            method = math.prod
        elif cur == '(':
            expr, sub = subexpr(expr)
            sub = evaluate_left_to_right(sub)
            total = sub if total is None and method is None else method((total, sub))
        else:
            total = int(cur) if total is None and method is None else method((total, int(cur)))

    return total


def evaluate_addition_first(expr):

    expr = expr.replace(' ', '')

    if any(char in expr for char in ['(', '+']):

        while '(' in expr:
            _, sub = subexpr(expr[expr.index('('):])
            expr = expr.replace(sub, str(evaluate_addition_first(sub[1:-1])))

        while (match := ADDITION.match(expr)):
            expr = expr.replace(
                match.group(1),
                str(sum(int(n) for n in match.group(1).split('+')))
            )

    return math.prod(int(c) for c in expr.split('*'))


def subexpr(expr):
    sub = ''

    if isinstance(expr, list):
        match_count = 1
        while match_count != 0:
            cur = expr.pop()
            if cur == '(':
                sub += cur
                match_count += 1
            elif cur == ')':
                match_count -= 1
                sub += cur if match_count != 0 else ''
            else:
                sub += cur
    else:
        match = 0
        start = None
        end = None
        for i, c in enumerate(expr):
            if c == '(':
                if start is None:
                    start = i
                match += 1

            elif c == ')':
                match -= 1
                if match == 0:
                    end = i + 1
                    break

        sub = expr[start:end]

    return expr, sub


if __name__ == '__main__':
    test = '1 + 2 * 3 + 4 * 5 + 6'
    assert evaluate_left_to_right(test) == 71
    assert evaluate_addition_first(test) == 231

    test = '1+ (2 * 3) + (4 * (5 + 6))'
    assert evaluate_left_to_right(test) == 51
    assert evaluate_addition_first(test) == 51

    test = '2 * 3 + (4 * 5)'
    assert evaluate_left_to_right(test) == 26
    assert evaluate_addition_first(test) == 46

    test = '5 + (8 * 3 + 9 + 3 * 4 * 3)'
    assert evaluate_left_to_right(test) == 437
    assert evaluate_addition_first(test) == 1445

    test = '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'
    assert evaluate_left_to_right(test) == 12240
    assert evaluate_addition_first(test) == 669060

    test = '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'
    assert evaluate_left_to_right(test) == 13632
    assert evaluate_addition_first(test) == 23340


    with open('inputs/day18.txt') as f:
        expressions = [l.strip() for l in f.readlines() if l]

    assert sum(evaluate_left_to_right(expr) for expr in expressions) == 45283905029161
    assert sum(evaluate_addition_first(expr) for expr in expressions) == 216975281211165
