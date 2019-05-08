import socket as sk

import Constants
from Client import ClientThreadCallbacks

raps_socket = None


def fetch_home_info():
    raps_socket.send(b"0")
    data = raps_socket.recv(1024).decode()
    data = remove_string_fillers(data)
    print("Home info:", data)

    return data


def remove_string_fillers(string):
    return str(string).replace(Constants.trash_symbol, "")


def connect_to_raspberry(ip, port):
    global raps_socket
    raps_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    raps_socket.connect((ip, port))

    print("Connected to Raspberry")
