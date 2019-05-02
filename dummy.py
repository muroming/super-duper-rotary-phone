import socket as sk
import urllib.request as req

from Client.ClientThread import image_chunk_size


def login_user_test(s):
    s.send(b"0")
    s.send(b"testuser testpassword")
    print("All sent")
    print(s.recv(1024).decode())


def create_user_test(s):
    s.send(b"2")
    s.send(b"testname testuser testpassword")
    print("All sent")
    print(s.recv(1024).decode())


def send_pic_test(s):
    s.send(b"4")
    with open('me.jpg', 'rb') as f:
        bytes = f.read()
        current_chunk = 0
        while current_chunk < len(bytes) // image_chunk_size:
            data = bytes[current_chunk
                         * image_chunk_size:(current_chunk + 1) * image_chunk_size]
            print("Bytes sent:", len(bytes))
            s.send(data)
            current_chunk += 1

        print("Last chunk")
        data = bytes[current_chunk * image_chunk_size:]
        print("Bytes sent:", len(bytes))
        s.send(data)


def authorize_user_test(s):
    s.send(b"3")
    with open('me.jpg', 'rb') as f:
        bytes = f.read()
        current_chunk = 0
        while current_chunk < len(bytes) // image_chunk_size:
            data = bytes[current_chunk
                         * image_chunk_size:(current_chunk + 1) * image_chunk_size]
            print("Bytes sent:", len(bytes))
            s.send(data)
            current_chunk += 1

        print("Last chunk")
        data = bytes[current_chunk * image_chunk_size:]
        print("Bytes sent:", len(bytes))
        s.send(data)
    print(s.recv(1024).decode())


s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
s.connect(("127.0.0.1", 3456))

authorize_user_test(s)
