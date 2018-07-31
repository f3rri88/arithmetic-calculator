from collections import namedtuple
import re


Tok = namedtuple('Tok', 'name value')


class with_current(object):

    def __init__(self, f):
        self._f = f

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.current = next(self._gen)
        except StopIteration:
            self.current = None
        return self.current

    def __call__(self, *args, **kw):
        self._gen = self._f(*args, **kw)
        return self

    def __repr__(self):
        return '{}(current={})'.format(self._f.__name__, str(self.current))


@with_current
def tokenize(source):
    pattern = re.compile(r"\s*(?:(\d+)|(.))")
    for number, operator in pattern.findall(source):
        if number:
            yield Tok('NUMBER', number)
        else:
            yield Tok('BINOP', operator)


PRECEDENCE_MAP = {
    '+':    1,
    '-':    1,
    '*':    2,
    '/':    2,
}


def compute_atom(tokenizer):
    tok = tokenizer.current
    if tok is None:
        raise SyntaxError('Operation ended unexpectedly')
    elif tok.name == 'BINOP':
        raise SyntaxError(
            'Expected an operand, not an operator "{}"'.format(tok.value))
    else:
        assert tok.name == 'NUMBER'
        next(tokenizer)
        return int(tok.value)


def compute_expr(tokenizer, min_prec):
    atom_lhs = compute_atom(tokenizer)

    while True:
        cur = tokenizer.current
        if (cur is None or
                cur.name != 'BINOP' or
                PRECEDENCE_MAP[cur.value] < min_prec):
            break

        # Inside this loop the current token is a binary operator
        assert cur.name == 'BINOP'

        # Get the operator's precedence and associativity, and compute a
        # minimal precedence for the recursive call
        op = cur.value
        prec = PRECEDENCE_MAP[op]
        next_min_prec = prec + 1

        # Consume the current token and prepare the next one for the
        # recursive call
        next(tokenizer)
        atom_rhs = compute_expr(tokenizer, next_min_prec)

        # Update lhs with the new value
        atom_lhs = compute_op(op, atom_lhs, atom_rhs)

    return atom_lhs


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


def compute(op):
    t = tokenize(op)
    next(t)
    return compute_expr(t, 1)
