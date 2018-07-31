from server.calculation.tokenize import tokenize


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

    cur = tokenizer.current
    while (cur is not None and
            cur.name == 'BINOP' and
            PRECEDENCE_MAP[cur.value] >= min_prec):

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
        cur = tokenizer.current

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
