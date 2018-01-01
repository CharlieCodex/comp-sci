from utils import *
import readline
from cmd_line_tools import *
import socket_demo


def main_loop(state):
    while state.running:
        if state.process == '__main__':
            raw = input('| ').split(' ')
            # evaluate the new raw input on the root process
            cmd = raw[0]
            args = raw[1:]
            # split input into a command and arguments
            if cmd in state.commands:
                # pass the args into the command
                try:
                    state = state.commands[cmd]._eval_(state, *args)
                except Exception as e:
                    state.commands[cmd]._err_(e)
            else:
                color_print('Command not recognized', 'red')
        else:
            raw = input('({}) | '.format(state.process)).split(' ')
            # evaluate the new raw input on the current process
            try:
                state = state.processes[state.process]._eval_(state, raw)
            except Exception as e:
                state.processes[state.process]._err_(e)


class EchoProcess(Process):
        def __init__(self):
            super().__init__('echo')
            self.data = []

        def _transfer_(self, state, *args):
            super()._transfer_(state, *args)
            print('Welcome to echo!')
            return state

        def _eval_(self, state, raw):
            if 'exit' in raw:
                state = super()._untransfer_(state, raw)
                return state
            self.data.append(', '.join(raw))
            print('\n'.join(self.data))
            return state

        def _err_(self, err):
            print(err)


if __name__ == '__main__':
    def _exit(state, *args):
        state.running = False
        return state

    def _help(state, *args):
        for cmd in state.commands:
            print(cmd)
        return state

    commands = {
        'exit': Command('exit', _exit),
        'help': Command('help', _help)
    }
    processes = {
        'echo': EchoProcess(),
        'tic': socket_demo.TicTacToe()
    }
    state = State(commands, processes)
    main_loop(state)
