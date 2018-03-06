from readline import *
from parser import Parser
from state import State


def repl():
    running = True
    state = State()
    while running:
        line = input('- > ')
        if line == '.exit':
            running = False
            break
        parser = Parser(line, state)
        parser.read()
        parser.eval()
        state = parser.state


if __name__ == '__main__':
    repl()
