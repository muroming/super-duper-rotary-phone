import json
import socket as sk
import sys

from Client import ClientSessions, ClientThreadCallbacks
from Client.ClientThread import ClientThread
from NeuralNets.FaceRecognition.Recognition import person_faces_amount
from SocketThread import SocketThread

QTOKEN = "token"
QIMG_SIZE = "img_size"
QUSER_NAME = "user_name"
QUSER_LOGIN = "user_login"
QUSER_PASSWORD = "user_password"

ip_address = ""
serversocket_port = 8888

serversocket = None


def main():
    global serversocket
    serversocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    serversocket.bind((ip_address, serversocket_port))
    serversocket.listen(10)

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
