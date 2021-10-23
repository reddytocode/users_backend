import pymongo
from flask import Flask, request
from DB_client import mongo, init_mongo
from models.Atleta import Atleta
from flask_pymongo import PyMongo
from flask import jsonify
from User import User


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://balboa:balboa@cluster0.upvhr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongo = PyMongo(app)


@app.route("/registro", methods=["POST"])
def registro():
    content = request.json
    atleta = Atleta(**content)
    res = atleta.save(mongo)
    return jsonify(**res)


@app.route('/user/save', methods=["POST"])
def saveUser():
    content = request.json
    user = User()
    user.create(**content)
    res = user.save(mongo)
    return jsonify(**res)


@app.route('/users')
def getAllUsers():
    return jsonify(users=User.getAll(mongo))


@app.route('/user/<ci>', methods=["DELETE"])
def remove_user(ci):
    return jsonify(User.remove(mongo, ci))


def gen_message(msg):
    return jsonify(message=msg)


@app.route("/login", methods=["POST"])
def login():
    content = request.json
    atleta = Atleta.find_by_email(mongo, content["email"])
    if content["password"] == atleta.password:
        return gen_message("Bienvenido")
    return gen_message("Wrong Password")


if __name__ == '__main__':
    app.run(debug=True, port=5002)
