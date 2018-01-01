import numpy as np


class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def get_color(cls, color):
        if color.upper() in cls.__dict__:
            return cls.__dict__[color.upper()]
        else:
            return cls.ENDC


def color_print(text, color):
    print(bcolors.get_color(color) + text + bcolors.ENDC)


def color_prints(text, color):
    return bcolors.get_color(color) + text + bcolors.ENDC


def phase_interference(a, b):
    return 4 * np.sqrt(2 + 2 * np.cos(a - b))
