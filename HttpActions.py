import json
import time
from sqlite3 import IntegrityError
from threading import Thread

import Constants
import ServerToRasp
from Client import ClientSessions, ClientThreadCallbacks
from Client.ClientThread import ClientThread
from NeuralNets.FaceRecognition.Recognition import person_faces_amount
from StringUtils import remove_string_fillers


def fetch_home_info():
    print("Fething home data from Raspberry")
    data = ServerToRasp.fetch_home_info()
    return data


def fetch_avaliable_home_items(login):
    print("Fetching avaliable items for user", login)
    items = ClientSessions.fetch_user_items(login)
    items = json.dumps(items, default=lambda x: x.__dict__)

    if Constants.is_debug:
        print(items)

    return items


def add_photos(client_socket):
    username = remove_string_fillers(client_socket.recv(1024).decode())
    print("Adding photos for user:", username)
    print("Sending total photos requiered:", person_faces_amount)
    client_socket.send(("201" + str(person_faces_amount)).encode())
    return ClientThread(client_socket, ClientThreadCallbacks.add_user_photo_callback, username=username)


def create_user(user_name, user_login, user_password):
    print("Creating user", user_name, user_login, user_password)
    try:
        user = ClientSessions.create_user(user_name, user_login, user_password)
        return '', 200 if user is not None else 'Internal error', 500
    except IntegrityError:
        return Constants.user_already_exists, 500


def login_user(user_login, user_password):
    print("Logining user:", user_login, user_password)
    user = ClientSessions.login_user(user_login, user_password)
    return Constants.successful_response if user is not None else Constants.error_response


def logout_user(user_login, user_password):
    print("Login out user")
    user = ClientSessions.logout_user(user_login, user_password)
    return Constants.successful_response if user is not None else Constants.error_response


def validate_user(client_socket):
    print("Validating user")
    return ClientThread(client_socket, ClientThreadCallbacks.authorize_user, photo_attempts=6)


def toggle_item_power(id):
    print("Toggling")
    is_succ, new_state = ClientSessions.toggle_item_power(id)
    if new_state:   # Itemed turned on
        ServerToRasp.turn_item_on(id)
    else:
        ServerToRasp.turn_item_off(id)

    return Constants.successful_response if is_succ else Constants.error_response


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
    "6": fetch_avaliable_home_items,
    # TOGGLE ITEM POWER
    "7": toggle_item_power
}


class SocketThread(Thread):
    def __init__(self, client_socket, address, serve_forever=False):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.address = address
        self.serve_forever = serve_forever
        print("Starting socket thread for address:", address)
        self.start()

    def run(self):
        loop = True
        while loop:
            action = remove_string_fillers(self.client_socket.recv(1024).decode())
            print(action, actions[action])
            self.thread = actions[action](self.client_socket)
            loop = self.serve_forever
            if loop and self.thread is not None:
                self.thread.join()
        print("Socket thread done")
