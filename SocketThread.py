from threading import Thread

from Client import ClientSessions, ClientThreadCallbacks
from Client.ClientThread import ClientThread


def add_photos(client_socket):
    print("Adding photos")
    return ClientThread(client_socket, ClientThreadCallbacks.add_user_photo_callback, username="test_user")


def login_user(client_socket):
    print("Logining user")
    user_data = client_socket.recv(1024).decode()
    print(user_data)
    user_login, user_password = user_data.split(" ")
    user = ClientSessions.login_user(user_login, user_password)

    client_socket.send(
        b"Successful" if user is not None else b"User not found")


def create_user(client_socket):
    print("Creating user")
    user_data = client_socket.recv(1024).decode()
    print(user_data)
    user_name, user_login, user_password = user_data.split(" ")
    user = ClientSessions.create_user(user_name, user_login, user_password)

    client_socket.send(
        b"Successful" if user is not None else b"Something went wrong")


# Actions
actions = {
    # LOGIN_USER
    "0": login_user,
    # LOGOUT_USER
    "1": None,
    # CREATE_USER
    "2": create_user,
    # AUTHORIZE
    "3": None,
    # ADD_USER_PHOTOS
    "4": add_photos
}


class SocketThread(Thread):
    def __init__(self, client_socket, address):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.address = address
        print("Starting server socket for address:", address)
        self.start()

    def run(self):
        action = self.client_socket.recv(1).decode()
        print(action)
        self.thread = actions[action](self.client_socket)

    def stop_connection(self):
        self.client_socket.close()
        if self.thread is not None:
            self.thread.stop_connection()
