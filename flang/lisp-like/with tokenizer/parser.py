from state import State
from primatives import Func, Expr


class Parser:
    def __init__(self, text, state=State()):
        self.text = text
        self.state = state
        self.stack = []
        self.errors = []
        self.char_num = 0

    def read(self, lines=1):
        lines_read = 0
        while lines_read < lines:
            self.whitespace()
            cur_char = self.current()
            if cur_char == '(':
                self.stack.append(self.read_expr())
            elif cur_char.isdigit():
                self.stack.append(self.read_int())
            else:
                self.stack.append(self.read_var())
            if not self.error():
                lines_read += 1

    def read_expr(self):
        # print('read expr')
        if not self.current() == '(':
            print('Syntax error, expected character \'(\'')
        self.next()
        self.whitespace()
        if self.current() == '(':
            func = self.read_expr()
        elif self.current().isdigit():
            func = self.read_int()
        else:
            func = self.read_var()
        args = []
        while self.next() != ')':
            self.whitespace()
            if self.current() == '(':
                args.append(self.read_expr())
            elif self.current().isdigit():
                args.append(self.read_int())
            else:
                args.append(self.read_var())
        return Expr(func, args)

    def read_func(self):
        if not self.current() == '[':
            print('Syntax error, expected character \'[\'')
        args = []
        while True:
            self.next()
            self.whitespace()
            if self.current() == ']':
                break
            else:
                args.append(self.read_param())
        self.next()
        self.whitespace()
        if not self.current() == '(':
            print('Syntax error, expected character \'(\'')
        func_body = self.read_expr()
        return Func(func_body, args)

    def read_var(self):
        # print('read var')
        if self.current() == '(':
            print('Syntax error, unexpected character \'(\',\
                   \nexpected identifier')
        identifier = ''
        while not(self.current().isspace() or self.finished()) and \
                not self.current() == ')':
            # print('finished?', self.finished())
            identifier += self.next()
        return self.state.ptr(identifier)

    def read_param(self):
        # print('read var')
        if self.current() == '(':
            print('Syntax error, unexpected character \'(\',\
                   \nexpected identifier')
        identifier = ''
        while not(self.current().isspace() or self.finished()) and \
                not self.current() == ')':
            # print('finished?', self.finished())
            identifier += self.next()
        return identifier

    def read_int(self):
        # print('read int')
        if self.current() == '(':
            print('Syntax error, unexpected character \'(\',\
                   \nexpected identifier')
        literal = ''
        while not(self.current().isspace() or self.finished()) and \
                not self.current() == ')':
            # print('finished?', self.finished())
            literal += self.next()

        return self.state.constant(int(literal))

    def whitespace(self):
        while self.current().isspace() or self.finished():
            # print('nexted in whitespace')
            self.next()

    def next(self):
        if len(self.text) <= self.char_num:
            return self.text[-1]
        char = self.text[self.char_num]
        self.char_num += 1
        return char

    def current(self):
        if len(self.text) <= self.char_num:
            return self.text[-1]
        return self.text[self.char_num]

    def finished(self):
        return len(self.text) <= self.char_num

    def eval(self):
        for expr in self.stack:
            if isinstance(expr, Expr):
                # print('got expr')
                expr.eval(self.state)
            else:
                # print('got var')
                print('< <', self.state.get(expr))

    def error(self):
        return self.errors.pop() if self.errors else None
