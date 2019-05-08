import sqlite3 as sql

from Client.Client import Client

DATABASE_NAME = "./Database/SMARTHOUSE_DATABASE"

USER_ACTIONS_TABLE_NAME = "USER_ACTIONS"
USERS_TABLE_NAME = "USERS"

USER_ACTIONS_TABLE = "%s (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_login TEXT NOT NULL, user_action TEXT NOT NULL, timestamp DATETIME NOT NULL)" % USER_ACTIONS_TABLE_NAME
USERS_TABLE = "%s (user_name TEXT PRIMARY KEY NOT NULL, user_login TEXT NOT NULL, user_password TEXT NOT NULL)" % USERS_TABLE_NAME

USER_ACTIONS_INSERT_NO_ID = "%s (user_login, user_action, timestamp)" % USER_ACTIONS_TABLE_NAME
USERS_TABLE_INSERT = "%s (user_name, user_login, user_password)" % USERS_TABLE_NAME

CHECK_TABLE_ACTION = "CREATE TABLE IF NOT EXISTS %s"

INSERT_ACTION = "INSERT INTO %s VALUES(?, ?, ?)" % USER_ACTIONS_INSERT_NO_ID
INSERT_USER = "INSERT INTO %s VALUES (?, ?, ?)" % USERS_TABLE_INSERT

FIND_ACTIONS_BY_LOGIN = "SELECT * FROM %s WHERE user_login=?" % USER_ACTIONS_TABLE_NAME
FIND_USER_BY_LOGIN = "SELECT * FROM %s WHERE user_login=?" % USERS_TABLE_NAME
FIND_USER_BY_LOGIN_PASSWORD = "SELECT * FROM %s WHERE user_login=? AND user_password=?" % USERS_TABLE_NAME


def get_connection():
    return sql.connect(DATABASE_NAME)


def check_tables():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(CHECK_TABLE_ACTION % USER_ACTIONS_TABLE)
    cursor.execute(CHECK_TABLE_ACTION % USERS_TABLE)
    con.commit()


def insert_user_action(client_login, client_action, timestamp):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(INSERT_ACTION, (client_login, client_action, timestamp))
    con.commit()


def get_user_actions_by_login(client_login):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(FIND_ACTIONS_BY_LOGIN, client_login)
    vals = cursor.fetchone()
    print("Save_user:", vals)
    if len(vals) == 0:
        return None

    name, login, password = vals
    return Client(name, login, password)


def save_user(name, login, password):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(INSERT_USER, (name, login, password))
    con.commit()
    cursor.execute(FIND_USER_BY_LOGIN_PASSWORD, (login, password))
    vals = cursor.fetchone()
    print("Save_user:", vals)
    if len(vals) == 0:
        return None

    name, login, password = vals
    return Client(name, login, password)


def get_user_by_login(user_login):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(FIND_USER_BY_LOGIN, user_login)
    name, login, password = cursor.fetchone()
    return Client(name, login, password)


def login_user(login, password):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(FIND_USER_BY_LOGIN_PASSWORD, (login, password))
    vals = cursor.fetchone()
    print("Login_user", vals)
    if vals == None:
        return None

    name, login, password = vals
    return Client(name, login, password)


check_tables()
