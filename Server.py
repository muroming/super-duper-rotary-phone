import socket as sk
import threading

from flask import Flask, request

from NeuralNets.FaceRecognition.Recognition import extract_face_from_image

app = Flask(__name__)

users = []
QTOKEN = "token"
QIMG_SIZE = "img_size"

image_port = 3456
token_connections = 3  # How many tries to connect to socket via token

connections = set()


@app.route("/")
def hello():
    return "Hello, world!"


@app.route("/get_users")
def get_all_users():
    return str(users)


@app.route("/add_user")
def add_user():
    token = request.args.get(QTOKEN)
    token_size = len(token.encode())
    img_size = request.args.get(QIMG_SIZE)

    print("Expected token:", token, "of size", token_size)

    serversocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    serversocket.bind(("127.0.0.1", image_port))
    serversocket.listen(1)
    print("listening on: %s:%d" % ("127.0.0.1", image_port))

    socket_thread = threading.Thread(
        target=handle_add_user_query, args=(serversocket, token, token_size))

    socket_thread.daemon = True
    connections.add(serversocket)
    socket_thread.run()


def handle_add_user_query(serversocket, token, token_size=1024):
    print("Started handler for:", serversocket)
    clientsocket, address = serversocket.accept()

    connection_tries = 0
    is_connected = False
    while connection_tries < token_connections and not is_connected:
        received_token = clientsocket.recv(token_size)
        connection_tries += 1

        decoded_token = ''.join('{:02x}'.format(x) for x in received_token)
        is_connected = decoded_token == token
        if connection_tries == token_connections and not is_connected:
            return

    print("Connected")


if __name__ == "__main__":
    app.run(debug=True)
