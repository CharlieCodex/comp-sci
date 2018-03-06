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

        self.assign('print', _print)
        self.assign('+', lambda state, x, y: x + y)
        self.assign('-', lambda state, x, y: x - y)
        self.assign('*', lambda state, x, y: x * y)
        self.assign('/', lambda state, x, y: x / y)

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
