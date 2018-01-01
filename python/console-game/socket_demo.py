import socket
from cmd_line_tools import *
from enum import Enum
import json
from sys import getsizeof


def send_json(sock, data):
    msg = json.dumps(data).encode()
    sock.send(bytes(msg))
    return getsizeof(bytes(msg))


def recv_json(sock, size=1024):
    msg = sock.recv(size)
    return json.loads(msg)


def gethostname():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8', 80))
    hostname = sock.getsockname()
    sock.close()
    return hostname


class TicTacToe(Process):
    """TicTacToe Process"""
    PORT = 1238

    class Tile(Enum):
        EMPTY = 0
        X = 1
        O = -1

    class Board():
        def __init__(self):
            self.state = [[TicTacToe.Tile.EMPTY for i in range(3)]
                          for j in range(3)]

        def put(self, player, x, y):
            """Put move on the board if it is a valid move"""
            # flip [x,y] to [y][x] as our array is arranged as a list of rows
            if self.state[y][x] == TicTacToe.Tile.EMPTY:
                tile = TicTacToe.Tile.X if player else TicTacToe.Tile.O
                self.state[y][x] = tile
                return True
            return False

        def render(self):
            for i, row in enumerate(self.state):
                msg = ' '
                for j, tile in enumerate(row):
                    if j != 0:
                        msg += ' | '
                    if tile == TicTacToe.Tile.X:
                        msg += color_prints('X', 'red')
                    elif tile == TicTacToe.Tile.O:
                        msg += color_prints('O', 'blue')
                    else:
                        msg += '.'
                print(msg)
                if i != 2:
                    print('-----------')

        def check(self):
            c = 0
            for i in range(3):
                for j in range(3):
                    if self.state[i][j] != TicTacToe.Tile.EMPTY:
                        c += 1
                        winner = self.state[i][j]
                        if self.state[(i - 1) % 3][j] == winner:
                            if self.state[(i - 2) % 3][j] == winner:
                                return winner
                        if self.state[i][(j - 1) % 3] == winner:
                            if self.state[i][(j - 2) % 3] == winner:
                                return winner
                        if i == j == 0:
                            if self.state[(i + 1) % 3][(j + 1) % 3] == winner and \
                               self.state[(i + 2) % 3][(j + 2) % 3] == winner:
                                return winner
                        if i == 0 and j == 2:
                            if self.state[(i + 1) % 3][(j - 1) % 3] == winner and \
                               self.state[(i + 2) % 3][(j - 2) % 3] == winner:
                                return winner
            return c < 9

    def __init__(self, parent=None):
        super().__init__('tic', parent)
        self.turn = True
        self.peerid = None
        self.peersock = None
        self.board = TicTacToe.Board()

    def _transfer_(self, state, *args):
        super()._transfer_(state, *args)
        if self.peersock:
            self.peersock.close()
        self.__init__(self.parent)
        self.run()
        if self.peersock:
            self.peersock.close()
        return super()._untransfer_(state, "")

    def run(self):
        if not self.establish_connection():
            assert Exception('Error establishing network connection')

        print('Welcome to TicTacToe, you are playing as',
              'X' if self.host else 'O')
        while not self.board.check():
            if self.turn == self.host:
                self.move()
            else:
                self.recv_move()
            self.board.render()
        winner = self.board.check()
        print('Winner is: ', winner)

    def move(self):
        x, y = self.get_move()
        self.send_move(x, y)

    def get_move(self):
        x = y = None
        while True:
            try:
                raw = input("It is your move, please "
                            "type in an address {{x, y}} to play:\n")
                if raw == 'exit':
                    assert Exception('Exit command entered')
                raw = raw.split(',')
                x = int(raw[0])
                y = int(raw[1])
                if 0 <= x <= 3 and 0 <= y <= 3 and \
                   self.board.put(self.host, x, y):
                    return x, y
                else:
                    x = y = None
            except Exception:
                print('Invalid input')

    def send_move(self, x, y):
        data = {'x': x, 'y': y}
        self.turn = not self.host
        send_json(self.peersock, data)

    def recv_move(self):
        print('Waiting for remote player to move')
        data = recv_json(self.peersock)
        x = data['x']
        y = data['y']
        self.board.put(not self.host, x, y)
        self.turn = self.host

    def establish_connection(self):
        host = input('Would you like to host a game (y, n)? ')
        host = host.lower() == 'y' or host.lower() == 'yes'
        self.host = host
        if self.host:
            connection = self.host_get_conn()
        else:
            connection = self.peer_get_conn()
        self.peersock = connection
        self.peerid = connection.getpeername()[0]
        if self.host:
            self.peersock.send(b'Start')
            return True
        else:
            res = self.peersock.recv(38)
            if res == b'Start':
                return True
        return False

    def host_get_conn(self):
        sock = socket.socket()
        addr = gethostname()[0]
        sock.bind((addr, TicTacToe.PORT))
        print('Waiting for a connection on {}'.format(addr))
        sock.listen(1)
        conn, _ = sock.accept()
        return conn

    def peer_get_conn(self):
        sock = socket.socket()
        ip = input('Host address? ')
        sock.connect((ip, TicTacToe.PORT))
        return sock

    def _eval_(self, state, raw):
        return super()._untransfer_(state, raw)


if __name__ == "__main__":
    tic = TicTacToe()
    tic.run()
