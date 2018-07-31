import re


def is_number(str):
    try:
        int(str)
        return True
    except ValueError:
        return False


def peek(stack):
    return stack[-1] if stack else None


def apply_operator(operators, values):
    operator = operators.pop()
    right = values.pop()
    left = values.pop()
    values.append(compute_op(operator, left, right))


def compute_op(op, lhs, rhs):
    if op == '+':
        return lhs + rhs
    elif op == '-':
        return lhs - rhs
    elif op == '*':
        return lhs * rhs
    elif op == '/':
        return lhs / rhs
    else:
        raise SyntaxError('This operator is not recognized "{}"'.format(op))


def compute(expression):
    tokens = re.findall(r"[+/*()-]|\d+", expression)
    precedences = {'+': 0, '-': 0, '*': 1, '/': 1}
    values = []
    operators = []
    for token in tokens:
        if is_number(token):
            values.append(int(token))
        elif token in precedences.keys():
            # Operator
            top = peek(operators)
            while (top is not None and
                    top not in "()" and
                    precedences[top] >= precedences[token]):
                apply_operator(operators, values)
                top = peek(operators)
            operators.append(token)
        else:
            raise SyntaxError('Element not recognized "{}"'.format(token))
    while peek(operators) is not None:
        apply_operator(operators, values)

    return values[0]
