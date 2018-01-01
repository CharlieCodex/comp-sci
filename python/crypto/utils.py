from ecc.key import Key
import json
import os.path

def safe_check(d, k, v):
    return k in d and d[k] == v

def to_binary(string):
    return bytes(string.encode('utf-8'))

def get_creds(name='mcv-seif'):
    homedir = os.path.expanduser('~')
    cred_file = homedir + '/.credentials/{}.json'.format(name)
    if os.path.isfile(cred_file):
        creds = get_creds_from_file(cred_file)
    else:
        creds = gen_creds(cred_file)
    if creds.validate():
        print("loaded creds",name)
        return creds
    else:
        raise ValueError("Credentials invalid; try deleting cached credentials", homedir + './credentials/mcv-seif.json')

def gen_creds(path):
    print('making new credentials')
    creds = Key.generate(521)
    write_creds(creds, path)
    return creds

def get_creds_fron_json(data):
    _priv = tuple(data['_priv'])
    _pub = tuple(data['_pub'])
    _pub = (_pub[0], tuple(_pub[1]))
    return Key(_pub, _priv)

def get_creds_from_file(path):
    print('loading credentials')
    with  open(path, 'r') as file:
        data = json.load(file)
        creds = get_creds_fron_json(data)
    return creds

def point_to_string(p):
    x, y = p
    string = str(x) + ',' + str(y)
    return string

def string_to_point(string):
    l = string.split(',')
    x = int(l[0])
    y = int(l[1])
    return (x, y)

def write_creds(creds, path):
    with open(path, 'w+') as file:
        json.dump({'_pub':creds._pub, '_priv':creds._priv}, file)

def encrypt_json_to_bytes(creds, data):
    msg = json.dumps(data)
    enc_msg = creds.encrypt(msg)
    enc_msg_bytes = to_binary(enc_msg)
    return enc_msg_bytes

def decrypt_json_from_bytes(creds, enc_msg_bytes):
    enc_msg = bytes.decode(enc_msg_bytes)
    msg = creds.decrypt(enc_msg)
    data = json.loads(msg)
    return data

