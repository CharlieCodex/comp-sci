class Expr:
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def eval(self, state):
        args = []
        for arg in self.args:
            if isinstance(arg, Expr):
                args.append(arg.eval(state))
            else:
                args.append(state.get(arg))
        return state.ptr_table.get(self.func)(state, *args)


class Func:
    def __init__(self, func_body, args):
        self.func_body = func_body
        self.args = args

    def eval(self, state, *func_args):
        local_state = state.create_substate()
        for arg, n in enumerate(self.args):
            local_state.assign(arg, func_args[n])
        return self.func_body.eval(local_state)
