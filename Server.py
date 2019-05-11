import socket as sk
import sys

import ServerToRasp
from SocketThread import SocketThread

QTOKEN = "token"
QIMG_SIZE = "img_size"
QUSER_NAME = "user_name"
QUSER_LOGIN = "user_login"
QUSER_PASSWORD = "user_password"

ip_address = ""
serversocket_port = 8887
rasp_ip = "192.168.43.26"
rasp_port = 8885

serversocket = None


def main():
    global serversocket
    serversocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    serversocket.bind((ip_address, serversocket_port))
    serversocket.listen(10)

    # print("Connecting to Raspberry")
    # ServerToRasp.connect_to_raspberry(rasp_ip, rasp_port)

    print("Server started")

    while True:
        client_socket, address = serversocket.accept()
        SocketThread(client_socket, address)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down, cleaning socket")
        if serversocket is not None:
            serversocket.close()
        print("Done")
        sys.exit(0)
