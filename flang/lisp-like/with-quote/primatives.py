class FuncCall:
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def eval(self, state):
        args = []
        for arg in self.args:
            if isinstance(arg, FuncCall):
                args.append(arg.eval(state))
            elif isinstance(arg, Func):
                args.append(arg)
            elif isinstance(arg, Quote):
                args.append(arg)
            else:
                args.append(state.get(arg))
        # print('Calling {} with {}'.format(self.func, args))
        if isinstance(self.func, FuncCall):
            self.func = self.func.eval(state)
        if isinstance(self.func, Func):
            return self.func(state, *args)
        return state.ptr_table.get(self.func)(state, *args)

    def __repr__(self):
        return '(' + repr(self.func) + ' ' + repr(self.args) + ')'


class Quote:
    def __init__(self, contents):
        # print('Created quote with contents {}'.format(contents))
        self.contents = contents

    def eval(self, state):
        contents = []
        for sym in self.contents:
            if callable(sym) or isinstance(sym, Func):
                contents.append(sym)
            elif isinstance(sym, FuncCall):
                contents.append(sym.eval(state))
            elif isinstance(sym, Quote):
                contents.append(sym.eval(state))
            else:
                contents.append(sym)
        func = state.get(contents[0])
        if callable(func) or\
           isinstance(func, Func):
            return FuncCall(func, contents[1:]).eval(state)
        return self

    def __repr__(self):
        return '`' + ', '.join(map(lambda x: repr(x), self.contents)) + '`'


class Func:
    def __init__(self, func_body, args):
        self.func_body = func_body
        self.args = args

    def eval(self, state, *func_args):
        local_state = state.create_substate()
        for n, arg in enumerate(self.args.contents):
            local_state.assign(arg, func_args[n])
        return self.func_body.eval(local_state)

    def __call__(self, state, *args):
        return self.eval(state, *args)

    def __repr__(self):
        return '[' + ', '.join(self.args.contents) + repr(self.func_body) + ']'


class PyFunc(Func):
    def __init__(self, pyfunc):
        self.func = pyfunc

    def eval(self, state, *args):
        return self.func(state, *args)

    def __repr__(self):
        return '[ PYTHON FUNC ' + repr(self.func.__name__) + ']'
