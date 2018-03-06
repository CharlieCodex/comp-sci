class Phrase:
    def __init__(self, precondition, read):
        self.cond = precondition
        self.readf = read

    def precondition(self, parser, buff):
        '''Overload this
           Return True/False on wheather or not this is a
           valid time to start reading this subphrase'''
        print('Overload this')
        return self.cond(parser, buff)

    def read(self, parser, buff):
        '''Overload this;
           Return an AstNode object'''
        print('Overload this')


class Interpreter:
    def __init__(self, state=''):
        pass


class AstNode:
    def __init__(self, name, node_type, data, children=[]):
        self.name = name
        self.node_type = node_type
        self.data = data
        self.children = children

    def add_child(self, node):
        if isinstance(node, AstNode):
            self.children.append(node)
        else:
            assert(TypeError('Child node must be an AstNode'))


class AstRoot(AstNode):
    def __init__(self):
        super().__init__(self, '__root__', '__root__')


class StringPhrase(Phrase):
    def __init__(self):
        super().__init__(self.precondition, self.read)

    def precondition(self, parser, buff):
        return buff.current == '"'

    def read(self, parser, buff):
        string = ''
        buff.next()
        while not(buff.finished() or buff.current() == '"'):
            # print('finished?', self.finished())
            if buff.current == '\\':
                buff.next()
            string += buff.current
            buff.next()
        return AstNode("StringNode", "__str_lit__", string)


class StringBuffer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current = text[0]

    def next(self):
        if self.pos < len(self.text) - 1:
            self.pos += 1
            self.current = self.text[self.pos]
        else:
            print('StringBuffer reached EOF')

    def finished(self):
        return not self.pos < len(self.text)

    def whitespace(self):
        while not (self.finished() or self.current.isspace()):
            self.next()


class Parser:
    def __init__(self, phrases):
        self.phrases = phrases
        self.ast_root = AstRoot()
        self.phrase_start = 0

    def read(self, text):
        if isinstance(text, str):
            buff = StringBuffer(text)
        elif isinstance(text, StringBuffer):
            buff = text
        else:
            assert(TypeError('Only str or StringBuffer are valid'
                             'formats for positional argument \'text\''))
        while not buff.finished():
            buff.whitespace()
            for ph in self.phrases:
                if ph.precondition(self, buff):
                    self.ast_root.append_child(ph.read(self, buff))
                    break

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
