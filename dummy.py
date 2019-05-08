import os
import socket as sk
import uuid

import cv2
from Client.ClientThread import image_chunk_size
from Client.ClientThreadCallbacks import trash_symbol


def login_user_test(s):
    s.send(b"0")
    s.send(fill_string("testuser testpassword", 1024).encode())
    print("All sent")
    print(s.recv(1024).decode())


def create_user_test(s):
    s.send(fill_string("2", 1024).encode())
    s.send(fill_string("testname testuser testpassword", 1024).encode())
    print("All sent")
    print(s.recv(1024).decode())


def send_pic_test(s):
    s.send(b"4")
    s.send(fill_string("testuser", 1024).encode())
    faces = int(s.recv(3).decode())
    print("Faces requiered:", faces)
    for _ in range(2):
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
        response = s.recv(2).decode()
        if response == "OK":
            faces -= 1
        print("Faces left:", faces)


def authorize_user_test(s):
    s.send(b"3")
    cap = cv2.VideoCapture(0)
    response = "UNF"
    while response == "UNF":
        # Capture frame-by-frame
        ret, frame = cap.read()

        filename = './cache/%s.jpg' % str(uuid.uuid4())
        cv2.imwrite(filename, frame)
        with open(filename, 'rb') as f:
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

        os.remove(filename)
        response = s.recv(1024).decode()

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def fill_string(data, length):
    return data + "^" * (length - len(data))


s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
s.connect(("127.0.0.1", 3456))

create_user_test(s)
