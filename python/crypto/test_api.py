from ecc.key import Key

k = Key.generate(521)
msg = b'Bunny'

enc = k.encrypt(msg)

dec = k.decrypt(enc)

print(msg)

print(enc.encode('utf-8','ignore'))

print(dec)