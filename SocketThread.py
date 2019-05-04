from threading import Thread

from Client import ClientSessions, ClientThreadCallbacks
from Client.ClientThread import ClientThread
from NeuralNets.FaceRecognition.Recognition import person_faces_amount


def add_photos(client_socket):
    username = remove_string_fillers(client_socket.recv(1024).decode())
    print("Adding photos for user:", username)
    print("Sending total photos requiered:", person_faces_amount)
    client_socket.send(str(person_faces_amount).encode())
    return ClientThread(client_socket, ClientThreadCallbacks.add_user_photo_callback, username=username)


def login_user(client_socket):
    print("Logining user")
    user_data = remove_string_fillers(client_socket.recv(1024).decode())
    print(user_data)
    user_login, user_password = user_data.split(" ")
    user = ClientSessions.login_user(user_login, user_password)

    client_socket.send(
        b"Successful" if user is not None else b"User not found")


def create_user(client_socket):
    print("Creating user")
    user_data = remove_string_fillers(client_socket.recv(1024).decode())
    print(user_data).decode()
    user_name, user_login, user_password = user_data.split(" ")
    user = ClientSessions.create_user(user_name, user_login, user_password)

    client_socket.send(
        b"Successful" if user is not None else b"Something went wrong")


def logout_user(client_socket):
    print("Login out user")
    user_data = remove_string_fillers(client_socket.recv(1024).decode())
    print(user_data)
    user_login, user_password = user_data.split(" ")
    user = ClientSessions.logout_user(user_login, user_password)

    client_socket.send(
        b"Successful" if user is not None else b"Something went wrong")


def validate_user(client_socket):
    print("Validating user")
    return ClientThread(client_socket, ClientThreadCallbacks.authorize_user)


def remove_string_fillers(string):
    return str(string).replace(ClientThreadCallbacks.trash_symbol, "")


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
        print(action, actions[action])
        self.thread = actions[action](self.client_socket)

    def stop_connection(self):
        self.client_socket.close()
        if self.thread is not None:
            self.thread.stop_connection()
