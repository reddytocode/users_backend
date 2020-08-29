from pymongo.cursor import Cursor


class Atleta():

    def __init__(self, nombre, email, password, deporte, altura, peso):
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
    def find(mongo):
        document = mongo.db["huellas"]["atleta"]
        res: Cursor = document.find({"nombre": "test"})
        for ans in res:
            print(
                ans
            )



    def save(self, mongo):
        self.find(mongo)
        document = mongo.db["huellas"]["atleta"]
        mydict:dict = self.to_json()
        x = document.insert_one(mydict)
        mydict.pop("_id", None)
        return mydict