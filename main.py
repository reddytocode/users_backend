import pymongo
from flask import Flask
from DB_client import mongo, init_mongo
from models.Atleta import Atleta
from flask_pymongo import PyMongo
from flask import jsonify


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://tesis:tesis@cluster0.r5ydz.mongodb.net/huellas?retryWrites=true&w=majority"
mongo = PyMongo(app)


@app.route("/")
def home_page():
    atleta = Atleta("test", "test", "password", "futbol", 1.87, 75.5)
    res = atleta.save(mongo)
    return jsonify(**res)


if __name__ == '__main__':
    app.run(debug=True)