import re
from collections import namedtuple


Tok = namedtuple('Tok', 'name value')


class with_current(object):
    '''
    Allows a generator function to recover current value
    by using current property
    '''
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
    '''
    Subdivides an arithmetical operation into operands and operators.
    tokenize(operation) -> generator
    '''
    pattern = re.compile(r"\s*(?:(\d+)|(.))")
    for number, operator in pattern.findall(source):
        if number:
            yield Tok('NUMBER', number)
        else:
            yield Tok('BINOP', operator)
