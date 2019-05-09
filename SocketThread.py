import json
import time
from threading import Thread

import Constants
import ServerToRasp
from Client import ClientSessions, ClientThreadCallbacks
from Client.ClientThread import ClientThread
from NeuralNets.FaceRecognition.Recognition import person_faces_amount


def fetch_home_info(client_socket):
    print("Fething home data from Raspberry")
    data = ServerToRasp.fetch_home_info()
    if len(data) == 0:
        data = Constants.error_response
    client_socket.send(data.encode())


def fetch_avaliable_home_items(client_socket):
    login = client_socket.recv(1024).decode()
    login = remove_string_fillers(login)
    print("Fetching avaliable items for user", login)
    items = ClientSessions.fetch_user_items(login)
    items = json.dumps(items, default=lambda x: x.__dict__)

    if len(items) != 0:
        items = Constants.successful_response + items
    else:
        items = Constants.error_response

    if Constants.is_debug:
        print(items)

    client_socket.send(items.encode())


def add_photos(client_socket):
    username = remove_string_fillers(client_socket.recv(1024).decode())
    print("Adding photos for user:", username)
    print("Sending total photos requiered:", person_faces_amount)
    client_socket.send(str(person_faces_amount).encode())
    return ClientThread(client_socket, ClientThreadCallbacks.add_user_photo_callback, username=username)


def create_user(client_socket):
    print("Creating user")
    user_data = remove_string_fillers(client_socket.recv(1024).decode())
    print(user_data)
    user_name, user_login, user_password = user_data.split(" ")
    user = ClientSessions.create_user(user_name, user_login, user_password)
    client_socket.send(Constants.successful_response.encode()
                       if user is not None else Constants.error_response.encode())


def login_user(client_socket):
    print("Logining user")
    user_data = remove_string_fillers(client_socket.recv(1024).decode())
    print(user_data)
    user_login, user_password = user_data.split(" ")
    user = ClientSessions.login_user(user_login, user_password)
    client_socket.send(Constants.successful_response.encode()
                       if user is not None else Constants.error_response.encode())


def logout_user(client_socket):
    print("Login out user")
    user_data = remove_string_fillers(client_socket.recv(1024).decode())
    print(user_data)
    user_login, user_password = user_data.split(" ")
    user = ClientSessions.logout_user(user_login, user_password)
    client_socket.send(Constants.successful_response.encode()
                       if user is not None else Constants.error_response.encode())


def validate_user(client_socket):
    print("Validating user")
    return ClientThread(client_socket, ClientThreadCallbacks.authorize_user)


def remove_string_fillers(string):
    return str(string).replace(Constants.trash_symbol, "")


# Actions
actions = {
    # LOGIN_USER
    "0": login_user,
    # LOGOUT_USER
    "1": logout_user,
    # CREATE_USER
    "2": create_user,
    # AUTHORIZE
    "3": validate_user,
    # ADD_USER_PHOTOS
    "4": add_photos,
    # FETCH_HOME_INFO
    "5": fetch_home_info,
    # FETCH_AVALIABLE_HOME_ITEMS
    "6": fetch_avaliable_home_items
}


class SocketThread(Thread):
    def __init__(self, client_socket, address):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.address = address
        print("Starting server socket for address:", address)
        self.start()

    def run(self):
        action = remove_string_fillers(self.client_socket.recv(1024).decode())
        print(action, actions[action])
        self.thread = actions[action](self.client_socket)
        print("Socket thread done")
