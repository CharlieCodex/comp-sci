from readline import *
from parser import Parser
from state import State
import traceback
import sys


def repl():
    running = True
    state = State()
    while running:
        line = input('- > ')
        if line == '.exit':
            running = False
            break
        if line[0] == '.':
            exec((line[1:]))
        else:
            parser = Parser(line, state)
            try:
                parser.read()
                parser.eval()
                state = parser.state
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                print('Error at char {}'.format(parser.char_num))


if __name__ == '__main__':
    repl()
    '''s = State()
    p = Parser('`(print 2)', s)
    p.read()
    print(p.stack)
    q = p.stack[0]
    print(q)
    print(q.eval(s))'''
