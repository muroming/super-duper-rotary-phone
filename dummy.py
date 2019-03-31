import socket as sk
import urllib.request as req

s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
s.connect(("127.0.0.1", 3456))
print('Connected')
s.send(b'test')
print('Sent')
