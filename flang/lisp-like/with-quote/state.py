from primatives import FuncCall, Quote, Func, PyFunc
import parser


class FillTable:
    def __init__(self):
        self.mem = []
        self.open = []

    def free(self, addr):
        self.open.append(addr)
        self.mem[addr] = None

    def push(self, data):
        if not len(self.open) == 0:
            addr = self.open.pop()
            self.mem[addr] = data
        else:
            self.mem.append(data)
            addr = len(self.mem) - 1
        return addr

    def get(self, addr):
        return self.mem[addr]


class State:
    def __init__(self):
        self.sym_table = {}
        self.ptr_table = FillTable()
        self.create_builtins()

    def create_builtins(self):
        def _print(state, *vals):
            print('< <', *vals)

        def _let(state, symbol, value):
            if isinstance(symbol, Quote):
                state.assign(symbol.contents[0], value)
            return value

        def _fn(state, args, body):
            return Func(body, args)

        def _load(state, *files):
            for file_ in files:
                file = file_.contents[0]
                with open(file, 'r') as f:
                    p = parser.Parser(f.read())
                    p.read()
                    p.eval()
                    load_state = p.state
                _let(state, file, load_state)

        self.assign('print', PyFunc(_print))
        self.assign('let', PyFunc(_let))
        self.assign('fn', PyFunc(_fn))
        self.assign('load', PyFunc(_load))
        self.assign('+', PyFunc(lambda state, x, y: x + y))
        self.assign('-', PyFunc(lambda state, x, y: x - y))
        self.assign('*', PyFunc(lambda state, x, y: x * y))
        self.assign('/', PyFunc(lambda state, x, y: x / y))

    def assign(self, sym, val):
        self.sym_table[sym] = self.ptr_table.push(val)

    def constant(self, data):
        if isinstance(data, int):
            addr = str(data) + 'int'
        else:
            addr = hash(data)
        self.assign(addr, data)
        return addr

    def free_sym(self, sym):
        addr = self.sym_table[sym]
        del self.sym_table[sym]
        self.ptr_table.free(addr)

    def get(self, sym):
        return self.ptr_table.get(self.sym_table[sym])

    def ptr(self, sym):
        return self.sym_table[sym]

    def create_substate(self):
        tmp = State()
        tmp.sym_table = dict(self.sym_table)
        tmp.ptr_table = self.ptr_table
        return tmp
