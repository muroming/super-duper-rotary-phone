import json
import socket as sk

from Client import ClientSessions, ClientThreadCallbacks
from Client.ClientThread import ClientThread
from NeuralNets.FaceRecognition.Recognition import person_faces_amount
from SocketThread import SocketThread

QTOKEN = "token"
QIMG_SIZE = "img_size"
QUSER_NAME = "user_name"
QUSER_LOGIN = "user_login"
QUSER_PASSWORD = "user_password"

ip_address = "127.0.0.1"
serversocket_port = 3456

connections = set()

serversocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
serversocket.bind((ip_address, serversocket_port))
serversocket.listen(10)

print("Server started")

while True:
    client_socket, address = serversocket.accept()
    connections.add(SocketThread(client_socket, address))


@app.route("/register_user")
def register_user():
    user_name = request.args.get(QUSER_NAME)
    user_login = request.args.get(QUSER_LOGIN)
    user_password = request.args.get(QUSER_PASSWORD)

    print(user_name, user_login, user_password)

    user = ClientSessions.create_user(user_name, user_login, user_password)

    return json.dump(user, default=lambda x: x.__dict__)
