from threading import Thread

from Client import ClientThreadCallbacks
from Client.ClientThread import ClientThread


def add_photos(client_socket):
    print("Strating client")
    return ClientThread(client_socket, ClientThreadCallbacks.add_user_callback, username="test_user")


# Actions
actions = {
    # LOGIN_USER
    "0": None,
    # LOGOUT_USER
    "1": None,
    # CREATE_USER
    "2": None,
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
