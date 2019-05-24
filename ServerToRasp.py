import random

from StringUtils import fill_string

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


def turn_item_on(item_id):
    print("Turning on item with id", item_id)
    raps_socket.send("3".encode())
    raps_socket.send(fill_string(item_id, 1024).encode())


def turn_item_off(item_id):
    print("Turning off item with id", item_id)
    raps_socket.send("4".encode())
    raps_socket.send(fill_string(item_id, 1024).encode())
