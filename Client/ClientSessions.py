import os
import pickle

from Client import Client

USER_DATA_DIR = os.path.join("", "UserData")
USERS = "users.pickle"

users = []
authenticated_users = []


def login_user(login, password):
    for user in users:
        if user.authorize(login, password):
            authenticated_users.append(user)
            return user

    return None


def logout_user(login, password):
    for user in authenticated_users:
        if user.authorize(login, password):
            authenticated_users.remove(user)
            return user

    return None


def create_user(name, login, password):
    user = Client.create_user(name, login, password)
    users.append(user)
    dump_database()

    return user


def dump_database():
    print(os.listdir('./'))
    users_file = open(os.path.join(USER_DATA_DIR, USERS), "wb")
    pickle.dump(users, users_file)


def load_users():
    global users
    if os.path.exists(USER_DATA_DIR) and os.path.exists(os.path.join(USER_DATA_DIR, USERS)) != 0:
        users_file = open(os.path.join(USER_DATA_DIR, USERS), "rb")
        users = pickle.load(users_file)

        for user in users:
            users.append(Client.Client(**user))

        print(users)
