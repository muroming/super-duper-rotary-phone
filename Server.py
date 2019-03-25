from flask import Flask, request

from NeuralNets.FaceRecognition.Recognition import extract_face_from_image

app = Flask(__name__)

users = []


@app.route("/")
def hello():
    return "Hello, world!"


@app.route("/get_users")
def get_all_users():
    return str(users)


@app.route("/add_user")
def add_user():
    name = request.args.get("username")
    users.append(name if name != None else "nu klass")
    return "ok"


if __name__ == "__main__":
    app.run(debug=True)
