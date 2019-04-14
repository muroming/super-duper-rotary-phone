import crypt

SALT = "lolqueq"


class Client():
    def __init__(self, name, login, password):
        self.name = name
        self.login = login
        self.password = password

    def authorize(self, login, password):
        return crypt.crypt(login, SALT) == self.login and crypt.crypt(password, SALT) == self.password


def create_user(name, login, password):
    return Client(name, crypt.crypt(login, SALT), crypt.crypt(password, SALT))
