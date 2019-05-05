import os
import pickle

from Database import Database

USER_DATA_DIR = os.path.join("Client", "UserData", "Authentication")
USERS = "users.pickle"

authenticated_users = []


def login_user(login, password):
    user = Database.login_user(login, password)
    if user is not None:
        authenticated_users.append(user)

    return user


def logout_user(login, password):
    for user in authenticated_users:
        if user.authorize(login, password):
            authenticated_users.remove(user)
            return user

    return None


def create_user(name, login, password):
    user = Database.save_user(name, login, password)

    return user
