import socket as sk
import sys

from flask import Flask, request

import HttpActions
import ServerToRasp
from NeuralNets.FaceRecognition.Recognition import TrainingThread

ip_address = ""
serversocket_port = 8887
rasp_ip = "192.168.43.26"
rasp_sender_port = 34567

serversocket = None
rasp_socket = None

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main_test_page():
    return "test page"


<<<<<<< HEAD
@app.route("/login", methods=["POST"])
=======
@app.route("/login", methods=["GET"])
>>>>>>> 34f7428510884101ac7e997ccd93256be4ebccd1
def login_user():
    user_login = request.args["user_login"]
    user_password = request.args["user_password"]
    return HttpActions.login_user(user_login, user_password)

<<<<<<< HEAD

@app.route("/home_info", methods=["GET"])
def fetch_home_info():
    return HttpActions.fetch_home_info()


@app.route("/avaliable_home_items", methods=["GET"])
def fetch_avaliable_home_items():
    user_login = request.args["user_login"]
    return HttpActions.fetch_avaliable_home_items(user_login)


@app.route("/create_user", methods=["POST"])
def create_user():
    user_login = request.args["user_login"]
    user_password = request.args["user_password"]
    user_name = request.args["user_name"]

    return HttpActions.create_user(user_name, user_login, user_password)


@app.route("/toggle_item_power", methods=["POST"])
def toggle_item_power():
    item_id = request.args["item_id"]
    return HttpActions.toggle_item_power(item_id)


@app.route("/logout", methods=["POST"])
def logout_user():
    user_login = request.args["user_login"]
    user_password = request.args["user_password"]
    return HttpActions.logout_user(user_login, user_password)

=======
>>>>>>> 34f7428510884101ac7e997ccd93256be4ebccd1

def main():
    global serversocket, rasp_socket
    serversocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    serversocket.bind((ip_address, serversocket_port))
    serversocket.listen(10)

    rasp_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    rasp_socket.bind((ip_address, rasp_sender_port))
    rasp_socket.listen(1)

    # Raspberry connecting listener thread
    print("Waiting for Raspberry listener thread...")
    socket, address = rasp_socket.accept()
    print("Starting Raspberry socket")
    SocketThread(socket, address, serve_forever=True)
    ServerToRasp.set_rasp_socket(socket)

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
    if len(sys.argv) != 1:
        args = sys.argv[1:]
        if args[0].lower() == "recognition":
            if args[1].lower() == "trainclf":
                TrainingThread()

        elif args[0].lower() == "database":
            from Database.Database import parse_args
            parse_args(args[1:])
    else:
        try:
            # TrainingThread()
            app.run(debug=True)
            # main()
        except KeyboardInterrupt:
            print("Shutting down, cleaning socket")
            if serversocket is not None:
                serversocket.close()

            if rasp_socket is not None:
                rasp_socket.close()
            print("Done")
            sys.exit(0)
