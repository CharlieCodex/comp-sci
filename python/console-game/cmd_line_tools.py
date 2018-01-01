from utils import *


class State:
    def __init__(self, commands={}, processes={}):
        self.commands = commands
        self.processes = processes
        self.process = '__main__'
        self.running = True
        self._add_builtins_()

    def _add_builtins_(self):
        self = self._add_command_(Command('trans', self._transfer_))

    def _add_process_(self, process):
        self.processes.update({process.name: process})

    def _add_command_(self, command):
        self.commands.update({command.name: command})

    @staticmethod
    def _transfer_(state, process, *args):
        if process in state.processes:
            state = state.processes[process]._transfer_(state, *args)
            return state
        else:
            color_print('No process named {}'.format(process), 'red')
        return state


def def_err(err):
    print(err)


class Command:
    def __init__(self, name, eval, err=def_err):
        self.name = name
        self._eval_ = eval
        self._err_ = err


class Process:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def _transfer_(self, state, *args):
        self.parent = state.process
        state.process = self.name
        print('Migrated from {} to {}'.format(self.parent, self.name))
        return state

    def _untransfer_(self, state, *args):
        state.process = self.parent
        print('Migrated from {} to {}'.format(self.name, self.parent))
        self.parent = None
        return state
