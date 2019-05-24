import os
import sqlite3 as sql
import sys

from Database.Client import Client
from Database.HomeItem import HomeItem

DATABASE_PATH = "/home/muroming/PythonProjects/SmartHouse/Database/SMARTHOUSE_DATABASE"

USER_ACTIONS_TABLE_NAME = "USER_ACTIONS"
USERS_TABLE_NAME = "USERS"
HOME_ITEMS_TABLE_NAME = "HOME_ITEMS"
ROLES_TABLE_NAME = "ROLES"
ACTIONS_TABLE_NAME = "ACTIONS"
AUTHENTICATED_USERS_TABLE_NAME = "AUTHENTICATED_USERS"

USER_ACTIONS_TABLE = "%s (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_login TEXT NOT NULL, user_action TEXT NOT NULL, timestamp DATETIME NOT NULL)" % USER_ACTIONS_TABLE_NAME
USERS_TABLE = "%s (user_name TEXT NOT NULL, user_login TEXT PRIMARY KEY NOT NULL, user_password TEXT NOT NULL, role TEXT NOT NULL)" % USERS_TABLE_NAME
HOME_ITEMS_TABLE = "%s (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, item_name TEXT NOT NULL, item_on INTEGER NOT NULL CHECK (item_on in (0, 1)), item_description TEXT, item_photo TEXT)" % HOME_ITEMS_TABLE_NAME
ROLES_TABLE = "%s (role_name TEXT PRIMARY KEY NOT NULL, interactable_items TEXT NOT NULL, actions TEXT)" % ROLES_TABLE_NAME
ACTIONS_TABLE = "%s (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, action_name TEXT NOT NULL)" % ACTIONS_TABLE_NAME
AUTHENTICATED_USERS_TABLE = "%s (user_login TEXT PRIMARY KEY NOT NULL)" % AUTHENTICATED_USERS_TABLE_NAME

USER_ACTIONS_INSERT_NO_ID = "%s (user_login, user_action, timestamp)" % USER_ACTIONS_TABLE_NAME
USERS_INSERT = "%s (user_name, user_login, user_password, role)" % USERS_TABLE_NAME
HOME_ITEM_INSERT_NO_ID = "%s (item_name, item_on, item_description, item_photo)" % HOME_ITEMS_TABLE_NAME
ROLES_INSERT = "%s (role_name, interactable_items, actions)" % ROLES_TABLE_NAME
ACTIONS_INSERT_NO_ID = "%s (action_name)" % ACTIONS_TABLE_NAME
AUTHENTICATED_USERS_INSERT = "%s (user_login)" % AUTHENTICATED_USERS_TABLE_NAME

CHECK_TABLE_ACTION = "CREATE TABLE IF NOT EXISTS %s"

INSERT_USER_ACTION = "INSERT INTO %s VALUES(?, ?, ?)" % USER_ACTIONS_INSERT_NO_ID
INSERT_USER = "INSERT INTO %s VALUES (?, ?, ?, ?)" % USERS_INSERT
INSERT_HOME_ITEM = "INSERT INTO %s VALUES (?, ?, ?, ?)" % HOME_ITEM_INSERT_NO_ID
INSERT_ROLE = "INSERT INTO %s VALUES (?, ?, ?)" % ROLES_INSERT
INSERT_ACTION = "INSERT INTO %s VALUES (?)" % ACTIONS_INSERT_NO_ID
INSERT_AUTHENTICATED_USER = "INSERT INTO %s VALUES(?)" % AUTHENTICATED_USERS_INSERT

FIND_ACTIONS_BY_LOGIN = "SELECT * FROM %s WHERE user_login=?" % USER_ACTIONS_TABLE_NAME
FIND_USER_BY_LOGIN = "SELECT * FROM %s WHERE user_login=?" % USERS_TABLE_NAME
FIND_USER_BY_LOGIN_PASSWORD = "SELECT * FROM %s WHERE user_login=? AND user_password=?" % USERS_TABLE_NAME
FIND_USER_ROLE_BY_LOGIN = "SELECT role FROM %s WHERE user_login=?" % USERS_TABLE_NAME
FIND_ROLE_BY_NAME = "SELECT * FROM %s WHERE role_name=?" % ROLES_TABLE_NAME
FIND_HOME_ITEM_BY_ID = "SELECT * FROM %s WHERE id=?" % HOME_ITEMS_TABLE_NAME
FIND_ACTION_BY_ID = "SELECT * FROM %s WHERE id=?" % ACTIONS_TABLE_NAME
FIND_AUTHENTICATED_BY_LOGIN = "SELECT * FROM %s WHERE user_login=?" % AUTHENTICATED_USERS_TABLE_NAME

DELETE_USER_BY_LOGIN = "DELETE FROM %s WHERE user_login=?" % USERS_TABLE_NAME
DELETE_ROLE_BY_NAME = "DELETE FROM %s WHERE role_name=?" % ROLES_TABLE_NAME
DELETE_ITEM_BY_ID = "DELETE FROM %s WHERE id=?" % HOME_ITEMS_TABLE_NAME
DELETE_USER_FROM_AUTHENTECATED = "DELETE FROM %s WHERE user_login=?" % AUTHENTICATED_USERS_TABLE_NAME

GET_ALL_QUERY = "SELECT * FROM %s"
DROP_TABLE = "DROP TABLE %s"

UPDATE_USER_ROLE_BY_LOGIN = "UPDATE %s SET role=? WHERE user_login=?" % USERS_TABLE_NAME
UPDATE_ITEM_POWER_BY_ID = "UPDATE %s SET item_on=? WHERE id=?" % HOME_ITEMS_TABLE_NAME


def get_connection():
    return sql.connect(DATABASE_PATH)


def get_cursor():
    return get_connection().cursor()


def check_tables():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(CHECK_TABLE_ACTION % USER_ACTIONS_TABLE)
    cursor.execute(CHECK_TABLE_ACTION % USERS_TABLE)
    cursor.execute(CHECK_TABLE_ACTION % HOME_ITEMS_TABLE)
    cursor.execute(CHECK_TABLE_ACTION % ROLES_TABLE)
    cursor.execute(CHECK_TABLE_ACTION % ACTIONS_TABLE)
    cursor.execute(CHECK_TABLE_ACTION % AUTHENTICATED_USERS_TABLE)

    con.commit()
    print("All tables now exist")


def insert(action, values):
    if type(values) != tuple:
        raise ValueError(tuple)

    con = get_connection()
    cursor = con.cursor()
    cursor.execute(action, values)
    con.commit()
    print("Inserted into", action.split(" ")[2], "values", values)


def get_user_actions_by_login(client_login):
    cursor = get_cursor()
    cursor.execute(FIND_ACTIONS_BY_LOGIN, (client_login,))
    vals = cursor.fetchone()
    print("Save_user:", vals)
    if len(vals) == 0:
        return None

    name, login, password, role = vals
    return Client(name, login, password)


def save_user(name, login, password, role="user"):
    cursor = get_cursor()
    insert(INSERT_USER, (name, login, password, role))
    # insert(INSERT_AUTHENTICATED_USER, (login,))
    cursor.execute(FIND_USER_BY_LOGIN_PASSWORD, (login, password))
    vals = cursor.fetchone()
    print("Save_user:", vals)
    if len(vals) == 0:
        return None

    name, login, password, role = vals
    return Client(name, login, password)


def get_user_by_login(user_login):
    cursor = get_cursor()
    cursor.execute(FIND_USER_BY_LOGIN, (user_login,))
    name, login, password, role = cursor.fetchone()
    return Client(name, login, password)


def login_user(login, password):
    cursor = get_cursor()
    cursor.execute(FIND_USER_BY_LOGIN_PASSWORD, (login, password))
    vals = cursor.fetchone()
    print("Login_user", vals)
    if vals is None:
        return None

    name, login, password, role = vals
    # insert(INSERT_AUTHENTICATED_USER, (login,))
    return Client(name, login, password)


def update_user_role_by_login(login, role):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(UPDATE_USER_ROLE_BY_LOGIN, (role, login))
    con.commit()


def toggle_item_power(id):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(FIND_HOME_ITEM_BY_ID, (id,))
    id, name, is_on, desc, photo = cursor.fetchone()

    if is_on == 0:
        print("Turning", name, "on")
        cursor.execute(UPDATE_ITEM_POWER_BY_ID, (1, id))
    else:
        print("Turning", name, "off")
        cursor.execute(UPDATE_ITEM_POWER_BY_ID, (0, id))
    con.commit()

    return not bool(is_on)


def get_user_home_items(user_login):
    cursor = get_cursor()
    cursor.execute(FIND_USER_ROLE_BY_LOGIN, (user_login,))
    role = cursor.fetchone()
    print(role)
    if role is None:
        return []

    cursor.execute(FIND_ROLE_BY_NAME, role)
    role_name, interaction_items, actions = cursor.fetchone()
    items = []
    for id in interaction_items.split(' '):
        cursor.execute(FIND_HOME_ITEM_BY_ID, (str(id),))
        id, item_name, is_on, item_description, item_photo = cursor.fetchone()
        print(id, item_name, is_on, item_description, item_photo)
        items.append(HomeItem(id, item_name, is_on, item_description, item_photo))

    return items


def drop_database():
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    print("Database dropped")


def get_all_items(name):
    cursor = get_cursor()
    print(GET_ALL_QUERY % name)
    cursor.execute(GET_ALL_QUERY % name)
    items = cursor.fetchall()
    for item in items:
        print(item)


def delete_user_by_login(user_login):
    con = get_connection()
    print("Deleting user", user_login)
    cursor = con.cursor()
    cursor.execute(DELETE_USER_BY_LOGIN, (user_login,))
    cursor.execute(DELETE_USER_FROM_AUTHENTECATED, (user_login, ))
    con.commit()


def delete_role_by_name(role_name):
    con = get_connection()
    print("Deleting role", role_name)
    cursor = con.cursor()
    cursor.execute(DELETE_ROLE_BY_NAME, (role_name, ))
    con.commit()


def delete_item_by_id(id):
    con = get_connection()
    print("Deleting item", id)
    cursor = con.cursor()
    cursor.execute(DELETE_ITEM_BY_ID, (id,))
    con.commit()


def delete_user_from_auth(login):
    con = get_connection()
    print("Deuath", login)
    cursor = con.cursor()
    cursor.execute(DELETE_USER_FROM_AUTHENTECATED, (login, ))
    con.commit()


def drop_table(name):
    con = get_connection()
    print("Dropping", name)
    cursor = con.cursor()
    cursor.execute(DROP_TABLE % name)
    con.commit()


def parse_args(args):
    if args[0].lower() == "drop":
        drop_database()
    elif args[0].lower() == "create":
        check_tables()

    elif args[0].lower() == "droptable":
        drop_table(args[1])

    elif args[0].lower() == "delete":
        if args[1].lower() == "userlogin":
            delete_user_by_login(args[2])
        if args[1].lower() == "rolename":
            delete_role_by_name(args[2])
        if args[1].lower() == "itemid":
            delete_item_by_id(args[2])
        if args[1].lower() == "authlogin":
            delete_user_from_auth(args[2])

    elif args[0].lower() == "get":
        if args[1].lower() == "items":
            get_all_items(HOME_ITEMS_TABLE_NAME)
        elif args[1].lower() == "roles":
            get_all_items(ROLES_TABLE_NAME)
        elif args[1].lower() == "actions":
            get_all_items(ACTIONS_TABLE_NAME)
        elif args[1].lower() == "users":
            get_all_items(USERS_TABLE_NAME)
        elif args[1].lower() == "auth":
            get_all_items(AUTHENTICATED_USERS_TABLE_NAME)

    elif args[0].lower() == "update":
        if args[1].lower() == "userrole":
            update_user_role_by_login(args[2], args[3])

    elif args[0].lower() == "insert":
        if args[1].lower() == "role":
            insert(INSERT_ROLE, tuple(args[2:]))
        elif args[1].lower() == "action":
            insert(INSERT_ACTION, tuple(args[2:]))
        elif args[1].lower() == "item":
            insert(INSERT_HOME_ITEM, tuple(args[2:]))
        elif args[1].lower() == "user":
            insert(INSERT_USER, tuple(args[2:]))


if __name__ == "__main__":
    parse_args(sys.argv[1:])
