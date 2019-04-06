import socket as sk
import urllib.request as req

from ClientThread import image_chunk_size

s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
s.connect(("127.0.0.1", 3456))
print('Connected')
s.send(b'test')
with open('blastoise-mega.jpg', 'rb') as f:
    bytes = f.read()
    current_chunk = 0
    while current_chunk < len(bytes) // image_chunk_size:
        s.send(bytes[current_chunk * image_chunk_size:(current_chunk + 1) * image_chunk_size])
        current_chunk += 1

    s.send(bytes[current_chunk * image_chunk_size:])
