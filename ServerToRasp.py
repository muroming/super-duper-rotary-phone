import random

from Client import ClientThreadCallbacks
from StringUtils import *

raps_socket = None


def fetch_home_info():
    # raps_socket.send(b"0")
    # data = raps_socket.recv(1024).decode()
    # data = remove_string_fillers(data)
    temp, hum = 23 + random.randint(-100, 150) / 100, 17 + random.randint(-150, 200) / 100
    data = " ".join([str(temp), str(hum)])
    print("Home info:", data)

    return data


def set_rasp_socket(socket):
    global raps_socket
    raps_socket = socket
