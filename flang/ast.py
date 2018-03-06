symbols = {
    ':': 'func',
    '.': 'var'
}


class Symbol:
    MATCH_NONE = 0
    MATCH_CONTAINS = 1
    MATCH_IS = 2

    def __init__(self, kw, ast_name=None, subparser=None):
        self.kw = kw
        if not ast_name:
            ast_name = kw
        self.ast_name = ast_name
        self.subparser = subparser

    def match(self, frag):
        contains = int(self.kw.startswith(frag))
        if len(frag) == len(self.kw):
            contains = Symbol.MATCH_IS
        return contains


class SymbolParser:
    def __init__(self, data='', symbols={}):
        self.data = data
        self.out = ''
        self.index = 0
        self.symbols = symbols

    def add_symbol(self, sym):
        self.symbols[sym.kw] = sym

    def has_next(self):
        return self.index < len(self.data)

    def next(self):
        self.index += 1
        if self.index > len(self.data):
            return None
        return self.data[self.index - 1]

    def parse(self):
        current_frag = ''
        sym_pool = list(self.symbols.values())
        while self.has_next():
            char = self.next()
            if not char.isspace():
                if current_frag:
                    current_frag += char
                    _sym_pool = [sym for sym in sym_pool
                                 if sym.match(current_frag)]
                else:
                    current_frag = char
                    _sym_pool = [sym for sym in sym_pool
                                 if sym.match(current_frag)]
                if not _sym_pool:
                    _sym_pool = [sym for sym in sym_pool
                                 if sym.match(current_frag[:-1]) ==
                                 Symbol.MATCH_IS]
                    if not len(_sym_pool) == 1:
                        msg = 'Identical keywords in same parser index: {}'
                        assert ValueError(msg.format(self.index), _sym_pool)
                    else:
                        sym = _sym_pool[0]
                        self.out += sym.ast_name + ' '
                        current_frag = ''
                        print('out', self.out)
                print(current_frag, _sym_pool)
            else:
                _sym_pool = [sym for sym in sym_pool
                             if sym.match(current_frag) == Symbol.MATCH_IS]
                if not len(_sym_pool) == 1:
                    msg = 'Identical keywords in same parser index: {}'
                    assert ValueError(msg.format(self.index))
                else:
                    sym = _sym_pool[0]
                    self.out += sym.ast_name + ' '
                    current_frag = ''
                    print('out', self.out)


def read_file(path):
    with open(path, 'r') as file:
        s = file.read()
    return s


def ast_expr(expr_s):
    """Create a sub abstract syntax tree
       from a string expression"""
    pass


if __name__ == '__main__':
    parser = SymbolParser(':x.x')
    parser.add_symbol(Symbol(':', 'lambda'))
    parser.add_symbol(Symbol('.', ':'))
    parser.parse()
    print(parser.data)
    print(parser.out)
