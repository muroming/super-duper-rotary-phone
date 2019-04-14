import os
import pickle

from Client import Client

USER_DATA_DIR = "UserData"
USER_NAMES = "names.pickle"
USER_LOGINS = "login.pickle"
USER_PASSWORDS = "passwords.pickle"

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

    return user


if len(os.listdir(os.path.join("Client", USER_DATA_DIR))) != 0:
    logins = open(os.path.join(USER_DATA_DIR, USER_LOGINS), "rb")
    logins = pickle.load(logins)

    passwords = open(os.path.join(USER_DATA_DIR, USER_PASSWORDS), "rb")
    passwords = pickle.load(passwords)

    names = open(os.path.join(USER_DATA_DIR, USER_NAMES), "rb")
    names = pickle.load(names)

    for name, login, password in zip(names, logins, passwords):
        users.append(Client.Client(name, login, password))
