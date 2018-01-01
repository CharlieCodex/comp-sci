from utils import *
from socket_utils import *
from ecc.key import Key
import socket
from stackless import tasklet

PORT = 4322

class McvEntity:
    def __init__(self, ip_addr, creds):
        self.ip_addr = ip_addr
        self.creds = creds

    @staticmethod
    def from_handshake(creds, handshake):
        peer_addr = None
        peer_creds = None
        if 'mcv_seif' in handshake and handshake['mcv_seif'] == 1:
            _pub = creds.decrypt(handshake['_pub']);
            peer_creds = Key((521,string_to_point(_pub))) 
            ip_msg = creds.decrypt(handshake['ip_msg'])
            if peer_creds.validate() and peer_creds.verify(to_binary(ip_msg), handshake['ip_sig']):
                print('Successful connection! from: ', ip_msg)
                peer_addr = ip_msg
            else:
                raise ValueError('Invalid handshake data, aborting')
        return McvEntity(peer_addr, peer_creds)


class McvClient:
    def __init__(self, ip_addr, creds, verbose=False):
        self.ip_addr = ip_addr
        self.creds = creds
        self.socket = None
        self.verbose = verbose

    def _create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, key, port=PORT):
        s = create_tcp_socket()

        if '_pub' in key:
            server_creds = key
        else:
            server_creds = Key(key)

        _, handshake_msg = create_handshake(self.ip_addr, self.creds, server_creds)
        if self.verbose:
            print('initializing connection with handshake size: ', len(handshake_msg))
        s.connect((host, port))
        s.send(handshake_msg)
        ret_handshake = decrypt_json_from_bytes(self.socket.recv(5120))
        return McvEntity.from_handshake(server_creds, host, ret_handshake).bind(s)


class McvServer:
    def __init__(self, ip_addr, creds):
        self.ip_addr = ip_addr
        self.creds = creds
        self.socket = None

    def _create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip_addr, PORT))

    def listen(self, n):
        if not self.socket:
            self._create_socket()
        self.socket.listen(n)

    def accept(self):
        s = create_tcp_socket()
        s.bind((self.ip_addr, PORT))
        conn, addr = self.socket.accept()
        data = conn.recv(5120)
        handshake = decrypt_json_from_bytes(self.creds, data)
        entity = McvEntity.from_handshake(self.creds, handshake)
        return entity
