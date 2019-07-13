from flask import Flask, request

import HttpActions
import Reciever


class MainReciever(Reciever):
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def main_test_page():
        return "test page"

    @app.route("/login", methods=["POST"])
    def login_user():
        user_login = request.args["user_login"]
        user_password = request.args["user_password"]
        return HttpActions.login_user(user_login, user_password)

    @app.route("/home_info", methods=["GET"])
    def fetch_home_info():
        return HttpActions.fetch_home_info()

    @app.route("/avaliable_home_items", methods=["GET"])
    def fetch_avaliable_home_items():
        user_login = request.args["user_login"]
        return HttpActions.fetch_avaliable_home_items(user_login)

    @app.route("/create_user", methods=["POST"])
    def create_user():
        user_login = request.args["user_login"]
        user_password = request.args["user_password"]
        user_name = request.args["user_name"]

        return HttpActions.create_user(user_name, user_login, user_password)

    @app.route("/toggle_item_power", methods=["POST"])
    def toggle_item_power():
        item_id = request.args["item_id"]
        return HttpActions.toggle_item_power(item_id)

    @app.route("/logout", methods=["POST"])
    def logout_user():
        user_login = request.args["user_login"]
        user_password = request.args["user_password"]
        return HttpActions.logout_user(user_login, user_password)

    def run(debug):
        global app
        app.run(debug)
