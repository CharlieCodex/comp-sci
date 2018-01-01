import socket
import utils
import ecc.encoding
from ecc.key import Key
import json

creds = utils.get_creds()
print('Loaded creds')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
my_addr = s.getsockname()[0]
s.close()
print('Local address: ',my_addr)

def fancy_shit(data):
    chunks = data.split(b',')
    print("found {} chunks".format(len(chunks)))
    keys = []
    vals = []
    result = {}
    for chunk in chunks:
        key = ""
        if chr(chunk[0]) == '"':
            print('starting key')
            for char in chunk[1:]:
                if chr(char) == '"':
                    break
                key += chr(char)
                print('building key: ', key)
            keys.append(key)
            print('added key: ', key)
            vals.append(chunk[len(key)+3:])
        else:
            vals[-1] += chunk
    if not len(keys) == len(vals):
        assert ValueError("Parsing Error, non equal number of keys and vals")
    print(vals)
    return {keys[n]: vals[n] for n in range(len(keys))}

def main():
    running = True
    while running:
        mode = input('Host? ').lower()
        if mode == 'y' or mode == 'yes' or mode == 'host':
            print('Local pub_key: ', utils.to_binary(ecc.encoding.enc_point(creds._pub[1])))
            TCP_IP = my_addr
            TCP_PORT = 4444
            BUFFER_SIZE = 2048  # Normally 1024, but we want fast response 
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((TCP_IP, TCP_PORT))
            s.listen(1)
            conn, addr = s.accept()
            print('Connection address:', addr)
            while 1:
                data = conn.recv(BUFFER_SIZE)
                if not data: break
                data_obj = fancy_shit(data)
                if 'mcv_seif' in data_obj:
                    msg = creds.decrypt(bytes.decode(data_obj['_pub']));
                    print(msg);
                    other_creds = Key((521,utils.string_to_point(msg))) 
                    ipmsg = creds.decrypt(bytes.decode(data_obj['ip_msg']))
                    print(other_creds.validate())
                    if other_creds.verify(data_obj['ip_msg'], bytes.decode(data_obj['ip_sig'])):
                        print('Successful connection!!!!!')
                        conn.close()
                        break
                print("(host) received data")
                conn.send(data) 
            conn.close()
            s.close()
            print('(host) socket closed')
        else:
            TCP_IP = input('ip_addr: ')
            TCP_PORT = 4444
            BUFFER_SIZE = 2048

            other_creds = Key((521,ecc.encoding.dec_point('áØÄ\x87ª`ÝÓ\x92\x8c\x9eh";ûX\x1cFÈ#Qn\x00î&7Lýùäj\ræ\x9c\x07{ºÃ\xadöâ\x10b,zta"\x18«q\x8b±\x00\x02Ucé(7\x8ax\tqtoM-,N\x0b\x04ÖÂÿAø\nWÕçH`[]3úJÕsaÓi~ä\x17·\xa0\x1e\x0c\x18¶Gb\x08}MÝ\x13l\x04\x8aÄåaËÞo\x9f¹\x95L\x7f?yÀr»\x1c\x8d')))

            if not other_creds.validate():
                print('Invalid host key')
                break

            enc_pub = other_creds.encrypt(utils.to_binary(utils.point_to_string(creds._pub[1])))
            signed_ip = creds.sign(utils.to_binary(my_addr))
            enc_ip = other_creds.encrypt(utils.to_binary(my_addr))

            MESSAGE = utils.to_binary('"mcv_seif":1,"_pub":{},"ip_sig":{},"ip_msg":{}'.format(enc_pub, signed_ip, enc_ip))
            print(fancy_shit(MESSAGE))
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(MESSAGE)
            data = s.recv(BUFFER_SIZE)
            s.close()
            print('(client) socket closed')

def test():
    p = creds._pub[1]
    print(p)
    msg = utils.point_to_string(p)
    print(msg)
    msg = utils.to_binary(msg)
    
    enc = creds.encrypt(msg)
    enc = utils.to_binary(enc)
    enc = bytes.decode(enc)
    
    msg = creds.decrypt(enc)
    print(msg)
    p = utils.string_to_point(msg)
    print(p)


if __name__ == "__main__":
    main()