from flask_pymongo import PyMongo
from pymongo.cursor import Cursor


def get_document(mongo):
    return mongo.db["huellas"]["atleta"]


class Atleta():

    def __init__(self, nombre=None, email=None, password=None, deporte=None, altura=None, peso=None, **args):
        self.id = ""
        self.nombre = nombre
        self.email = email
        self.password = password
        self.deporte = deporte
        self.altura = altura
        self.peso = peso

    def to_json(self):
        return {
            "nombre": self.nombre,
            "email": self.email,
            "password": self.password
        }

    @staticmethod
    def find_by_email(mongo: PyMongo, email: str):
        document = get_document(mongo)
        res: Cursor = document.find({"email": email})
        for ans in res:
            atleta = Atleta(**ans)
            if email == atleta.email:
                return atleta
        return None

    def save(self, mongo):
        document = get_document(mongo)
        atleta_searched = self.find_by_email(mongo, self.email)
        if atleta_searched is None:
            mydict:dict = self.to_json()
            x = document.insert_one(mydict)
            mydict.pop("_id", None)
            return mydict
        else:
            return {"message":"Email already exists"}