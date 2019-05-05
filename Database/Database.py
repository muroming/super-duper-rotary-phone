import sqlite3 as sql

from Client.Client import Client

con = None
DATABASE_NAME = "SMARTHOUSE_DATABASE"

USER_ACTIONS_TABLE_NAME = "USER_ACTIONS"
USERS_TABLE_NAME = "USERS"

USER_ACTIONS_TABLE = "%s (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, user_login VARCHAR NOT NULL, user_action VARCHAR NOT NULL, timestamp DATETIME NOT NULL)" % USER_ACTIONS_TABLE_NAME
USERS_TABLE = "%s (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, user_name VARCHAR NOT NULL, user_login VARCHAR NOT NULL, user_password VARCHAR NOT NULL)" % USERS_TABLE_NAME

CHECK_TABLE_ACTION = "CREATE TABLE IF NOT EXISTS %s"

INSERT_ACTION = "INSERT INTO %s VALUES(?, ?, ?)" % USER_ACTIONS_TABLE_NAME
INSERT_USER = "INSERT INTO %s VALUES (?, ?, ?)" % USERS_TABLE_NAME

FIND_ACTIONS_BY_LOGIN = "SELECT * FROM %s WHERE user_login=?" % USER_ACTIONS_TABLE_NAME
FIND_USER_BY_LOGIN = "SELECT * FROM %s WHERE user_login=?" % USERS_TABLE_NAME
FIND_USER_BY_LOGIN_PASSWORD = "SELECT * FROM %s WHERE user_login=? AND user_password=?" % USERS_TABLE_NAME


def connect():
    global con
    con = sql.connect(DATABASE_NAME)
    check_tables(con.cursor())


def check_tables(cursor):
    cursor.execute(CHECK_TABLE_ACTION % USER_ACTIONS_TABLE)
    cursor.execute(CHECK_TABLE_ACTION % USERS_TABLE)
    con.commit()


def insert_user_action(client_login, client_action, timestamp):
    cursor = con.cursor()
    cursor.execute(INSERT_ACTION, (client_login, client_action, timestamp))
    con.commit()


def get_user_actions_by_login(client_login):
    cursor = con.cursor()
    cursor.execute(FIND_ACTIONS_BY_LOGIN, client_login)
    return cursor.fetchall()


def save_user(name, login, password):
    cursor = con.cursor()
    cursor.execute(INSERT_USER, (name, login, password))
    con.commit()
    cursor.execute(FIND_USER_BY_LOGIN_PASSWORD, (login, password))
    vals = cursor.fetchall()
    if len(vals) == 0:
        return None

    id, name, login, password = cursor.fetchall()
    return Client(id, name, login, password)


def get_user_by_login(user_login):
    cursor = con.cursor()
    cursor.execute(FIND_USER_BY_LOGIN, user_login)
    id, name, login, password = cursor.fetchall()
    return Client(id, name, login, password)


def login_user(login, password):
    cursor = con.cursor()
    cursor.execute(FIND_USER_BY_LOGIN_PASSWORD, (login, password))
    vals = cursor.fetchall()
    if len(vals) == 0:
        return None

    id, name, login, password = cursor.fetchall()
    return Client(id, name, login, password)


connect()
