import json
import socket as sk

from flask import Flask, request

from Client import ClientSessions, ClientThreadCallbacks
from Client.ClientThread import ClientThread
from NeuralNets.FaceRecognition.Recognition import person_faces_amount

app = Flask(__name__)

QTOKEN = "token"
QIMG_SIZE = "img_size"
QUSER_NAME = "user_name"
QUSER_LOGIN = "user_login"
QUSER_PASSWORD = "user_password"

ip_address = "127.0.0.1"
image_port = 3456

connections = set()


@app.route("/get_users")
def get_all_users():
    return "todo"


@app.route("/register_user")
def register_user():
    user_name = request.args.get(QUSER_NAME)
    user_login = request.args.get(QUSER_LOGIN)
    user_password = request.args.get(QUSER_PASSWORD)

    print(user_name, user_login, user_password)

    user = ClientSessions.create_user(user_name, user_login, user_password)

    return json.dump(user, default=lambda x: x.__dict__)


@app.route("/add_photos")
def add_photos():
    token = request.args.get(QTOKEN)
    token_size = len(token.encode())
    img_size = request.args.get(QIMG_SIZE)

    # TODO: make one serversocket
    serversocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    serversocket.bind((ip_address, image_port))
    serversocket.listen(1)

    connections.add(ClientThread(
        serversocket, ClientThreadCallbacks.add_user_callback, token, username="test_user"))

    return "%d" % person_faces_amount


if __name__ == "__main__":
    app.run(debug=True)
