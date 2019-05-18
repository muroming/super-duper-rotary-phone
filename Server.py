import socket as sk
import sys

import ServerToRasp
from SocketThread import SocketThread

ip_address = ""
serversocket_port = 8883
rasp_ip = "192.168.43.26"
rasp_sender_port = 34563

serversocket = None
rasp_socket = None


def main():
    global serversocket, rasp_socket
    serversocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    serversocket.bind((ip_address, serversocket_port))
    serversocket.listen(10)

    # rasp_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    # rasp_socket.bind((ip_address, rasp_sender_port))
    # rasp_socket.listen(1)
    #
    # # Raspberry connecting listener thread
    # print("Waiting for Raspberry listener thread...")
    # socket, address = rasp_socket.accept()
    # print("Starting Raspberry socket")
    # SocketThread(socket, address, serve_forever=True)
    # ServerToRasp.set_rasp_socket(socket)

    print("Server started")

    while True:
        client_socket, address = serversocket.accept()
        if address[0] == rasp_ip:
            print("Connected to Raspberry")
            print("Starting Raspberry thread")
            # Raspberry connecting photo thread
            SocketThread(client_socket, address, serve_forever=True)
        else:
            SocketThread(client_socket, address)


if __name__ == "__main__":
    if (sys.argv) != 0:
        args = sys.argv[1:]
        from NeuralNets.FaceRecognition.Recognition import load_model
        if args[0].lower() == "recognition":
            if args[1].lower() == "trainclf":
                load_model()

        elif args[0].lower() == "database":
            from Database.Database import parse_args
            parse_args(args[1:])
    else:
        try:
            main()
        except KeyboardInterrupt:
            print("Shutting down, cleaning socket")
            if serversocket is not None:
                serversocket.close()

            if rasp_socket is not None:
                rasp_socket.close()
            print("Done")
            sys.exit(0)
