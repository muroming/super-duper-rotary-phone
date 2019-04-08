import socket as sk

from flask import Flask, request

from ClientThread import ClientThread
from ClientThreadCallbacks import *
from NeuralNets.FaceRecognition.Recognition import person_faces_amount

app = Flask(__name__)

users = []
QTOKEN = "token"
QIMG_SIZE = "img_size"

ip_address = "127.0.0.1"
image_port = 3456

connections = set()


@app.route("/get_users")
def get_all_users():
    return str(users)


@app.route("/add_user")
def add_user():
    token = request.args.get(QTOKEN)
    token_size = len(token.encode())
    img_size = request.args.get(QIMG_SIZE)

    # TODO: make one serversocket
    serversocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    serversocket.bind((ip_address, image_port))
    serversocket.listen(1)

    connections.add(ClientThread(serversocket, add_user_callback, token, username="test_user"))

    return "%d" % person_faces_amount


if __name__ == "__main__":
    app.run(debug=True)
