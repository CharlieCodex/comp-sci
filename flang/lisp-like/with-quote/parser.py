from state import State
from primatives import Func, FuncCall, Quote


class Parser:
    def __init__(self, text, state=State()):
        self.text = text
        self.state = state
        self.stack = []
        self.errors = []
        self.char_num = 0

    def read(self):
        while not self.finished():
            self.whitespace()
            cur_char = self.current()
            if cur_char == '(':
                self.stack.append(self.read_func_call())
            elif cur_char.isdigit():
                self.stack.append(self.read_int())
            elif cur_char == '`':
                self.stack.append(self.read_quote())
            else:
                self.stack.append(self.read_identifier())

    def read_func_call(self):
        # print('read expr')
        if not self.current() == '(':
            print('Syntax error, expected character \'(\'')
        self.next()
        self.whitespace()
        if self.current() == '(':
            func = self.read_func_call()
        elif self.current().isdigit():
            func = self.read_int()
        else:
            func = self.state.ptr(self.read_identifier())
        args = []
        while self.next() != ')':
            self.whitespace()
            if self.current() == '(':
                args.append(self.read_func_call())
            elif self.current() == '`':
                args.append(self.read_quote())
            # elif self.current() == '"':
            #     args.append(self.read_string())
            elif self.current().isdigit():
                args.append(self.read_int())
            else:
                args.append(self.read_identifier())
        return FuncCall(func, args)

    # def read_string(self):
    #     string = ''
    #     self.next()
    #     while not(self.finished() or self.current() == '"'):
    #         # print('finished?', self.finished())
    #         string += self.current()
    #         if self.current() == '\\':
    #             string += self.next()
    #             self.next()
    #     return string

    def read_quote(self):
        if not self.current() == '`':
            print('Syntax error, expected character \'`\' (back quote)')
        self.next()
        self.whitespace()
        if self.current() == "(":
            contents = []
            while not self.next() == ')':
                self.whitespace()
                if self.current() == '`':
                    contents.append(self.read_quote())
                if self.current() == "(":
                    contents.append(self.read_sub_quote())
                elif self.current().isdigit():
                    contents.append(self.read_int())
                else:
                    contents.append(self.read_identifier())
        else:
            contents = []
            if self.current().isdigit():
                contents.append(self.read_int())
            else:
                contents.append(self.read_identifier())
        return Quote([item for item in contents if not item == ''])

    def read_sub_quote(self):
        if self.current() == "(":
            contents = []
            while not self.next() == ')':
                self.whitespace()
                if self.current() == '`':
                    print("Cannot quote inside of quote, at char {}"
                          .format(self.cur_char))
                if self.current() == "(":
                    contents.append(self.read_sub_quote())
                elif self.current().isdigit():
                    contents.append(self.read_int())
                else:
                    contents.append(self.read_identifier())
        else:
            contents = []
            if self.current().isdigit():
                contents.append(self.read_int())
            else:
                contents.append(self.read_identifier())
        return Quote([item for item in contents if not item == ''])

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

    def read_identifier(self):
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
            if isinstance(expr, FuncCall):
                # print('got expr')
                print('< <', expr.eval(self.state))
            elif isinstance(expr, Quote):
                print(expr.contents)
            else:
                # print('got var')
                print('< <', self.state.get(expr))

    def error(self):
        return self.errors.pop() if self.errors else None
