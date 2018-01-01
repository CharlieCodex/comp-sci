def read_file(path):
    with open(path, 'r') as file:
        s = file.read()
    return s


def create_ast(s):
    lines = s.split('\n')
    for line in lines

def ast_expr(expr_s):
    """Create a sub abstract syntax tree
       from a string expression"""
    pass


if __name__ == '__main__':
    s = read_file('test.flang')
    create_ast(s)
