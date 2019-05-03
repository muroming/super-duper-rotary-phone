import sqlite3 as sql

con = None
DATABASE_NAME = "SMARTHOUSE_DATABASE"
USER_ACTIONS_TABLE_NAME = "USER_ACTIONS"
USER_ACTIONS_TABLE = "%s (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, user_login VARCHAR NOT NULL, user_action VARCHAR NOT NULL, timestamp DATETIME NOT NULL)" % USER_ACTIONS_TABLE_NAME


INSERT_ACTION = "INSERT INTO %s VALUES(%s)"
CHECK_TABLE_ACTION = "CREATE TABLE IF NOT EXISTS %s"
FIND_ACTIONS_BY_LOGIN = "SELECT * FROM %s WHERE user_login=%s" % (USER_ACTIONS_TABLE_NAME, "%s")


def connect():
    con = sql.connect(DATABASE_NAME)
    check_tables(con.cursor())


def check_tables(cursor):
    cursor.execute(CHECK_TABLE_ACTION % USER_ACTIONS_TABLE)


def insert_user_action(client_login, client_action, timestamp):
    cursor = con.cursor()
    cursor.execute(INSERT_ACTION % (USER_ACTIONS_TABLE,
                                    map_dict_to_values(client_login, client_action, timestamp)))


def get_user_actions_by_login(client_login):
    cursor = con.cursor()
    cursor.execute(FIND_ACTIONS_BY_LOGIN % client_login)
    return cursor.fetchall()


def map_dict_to_values(*args):
    args = map(str, args)
    return ",".join(args)


connect()
