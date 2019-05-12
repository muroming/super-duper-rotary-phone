from Database import Database

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


def toggle_item_power(id):
    try:
        Database.toggle_item_power(id)
        return True
    except Exception:
        return False


def create_user(name, login, password):
    return Database.save_user(name, login, password)


def fetch_user_items(login):
    return Database.get_user_home_items(login)
