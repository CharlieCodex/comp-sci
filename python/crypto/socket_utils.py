from mcv_socket import McvEntity
from utils import *
import socket
from ecc.key import Key
from stackless import tasklet
SIGNALING_PORT = 4500
SEIF_VERSION = 1


def create_handshake(local_addr, local_creds, peer_creds, verbose=False):
    enc_pub = peer_creds.encrypt(point_to_string(local_creds._pub[1]))
    signed_ip = local_creds.sign(to_binary(local_addr))
    enc_ip = peer_creds.encrypt(local_addr)

    handshake = {
        "mcv_seif": SEIF_VERSION,
        "transaction": 'handshake',
        "_pub": enc_pub,
        "ip_sig": signed_ip,
        "ip_msg": enc_ip
    }

    handshake_msg = encrypt_json_to_bytes(peer_creds, handshake)
    if verbose:
        print('Handshake size: ', len(handshake_msg))

    return handshake, handshake_msg


def validate_handshake(local_creds, remote_addr, handshake):
    peer_addr = None
    peer_creds = None
    if ('transaction' in handshake and
            handshake['transaction'] == 'handshake' and
            'mcv_seif' in handshake and
            handshake['mcv_seif'] == SEIF_VERSION):
        _pub = creds.decrypt(handshake['_pub'])
        peer_creds = Key((521, string_to_point(_pub)))
        ip_msg = creds.decrypt(handshake['ip_msg'])
        if peer_creds.validate() and \
           peer_creds.verify(to_binary(ip_msg), handshake['ip_sig']):
            print('Successful connection! from: ', ip_msg)
            peer_addr = ip_msg
        else:
            return False
    if peer_addr == remote_addr and peer_creds:
        return peer_creds
    else:
        return False


def create_tcp_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Connection:
    def __init__(self, local_entity, remote_entity, sock=None):
        self.local = local_entity
        self.remote = remote_entity
        self.socket = sock


class Peer:
    def __init__(self, addr, creds, sock=None):
        self.addr = addr
        self.creds = creds
        self.socket = sock


class PeerServer(Peer):
    def __init__(self, addr, creds, sock):
        Peer.__init__(self, addr, creds, sock)
        '''Create a new Signalling server
        0: host Peer object
        1: socket object'''
        self.running = None
        self.host = host
        self.sock = sock

    def stop(self):
        self.running = False

    def start(self, creds, handler):
        self.running = True
        task = tasklet(self.serve_signalling)(creds, handler)
        task.insert()

    def serve_signalling(creds, handler):
        while self.running:
            conn, addr = self.sock.accept()
            data = conn.recv(5120)
            handshake = decrypt_json_from_bytes(self.creds, data)
            peer_creds = validate_handshake(creds, addr, handshake)
            if peer_creds:
                peer_sock = create_tcp_socket()
                peer_sock.bind(self.host.addr, 0)
                peer_sock.listen(1)
                _, msg = create_handshake(self.host.addr,
                                          self.host.creds,
                                          addr,
                                          peer_creds,
                                          peer_sock.getsockname()[1])
                conn.send(msg)
                conn.close()


def connect_to_peer(local_addr, local_creds,
                    peer_addr, peer_creds,
                    port=SIGNALING_PORT, sock=None, verbose=False):
    if sock is None:
        sock = create_tcp_socket()

    if verbose:
        print('Starting signalling process to ', peer_addr)
        print('Creating handshake')

    _, handshake_msg = create_handshake(local_addr, local_creds,
                                        peer_creds, True)

    if verbose:
        print('Handshake created')
        print('Creating socket connection')

    sock.connect((peer_addr, port))
    sock.send(handshake_msg)

    if verbose:
        print('Handshake sent, waiting for response')

    res_msg = sock.recv(5120)
    res = decrypt_json_from_bytes(local_creds, res_msg)
    if peer_creds.verify(to_binary(peer_addr), res['ip_sig']):
        entity = McvEntity(peer_addr, peer_creds)

    return entity
