from pymongo.cursor import Cursor
from flask_pymongo import PyMongo
current_user = None


def get_document(mongo):
    return mongo.db["huellas"]["user"]


class Dedo:
    def to_json(self):
        return {
            "category": self.category,
            "distance": self.distance,
        }

    def __init__(self):
        self.category = None
        self.distance = 0

    def is_valid(self):
        valid = self.category is not None
        print("valid", self.category, "id", valid)
        return valid


class User:
    def to_json(self):
        return {
            "name": self.name,
            "lastName": self.lastName,
            "ci": self.ci,
            "fechaNac": self.fechaNac,
            "telf": self.telf,
            "genero": self.genero,
            "pulgar_i": self.pulgar_i,
            "anular_i": self.anular_i,
            "medio_i": self.medio_i,
            "indice_i": self.indice_i,
            "menhique_i": self.menhique_i,

            "pulgar_d": self.pulgar_d,
            "anular_d": self.anular_d,
            "medio_d": self.medio_d,
            "indice_d": self.indice_d,
            "menhique_d": self.menhique_d,
            # res
            "res_primer_analisis": self.res_primer_analisis,
            "formula_digital": self.formula_digital,
            # = {"arco": 0, "presilla": 0, "verticilo": 0}
            "categ": self.categ,
            "d10": self.d10,
            "sqtl": self.sqtl,
            "recomendacion1": self.recomendacion1,
            "recomendacion2": self.recomendacion2
        }

    @staticmethod
    def find_by_email(mongo: PyMongo, email: str):
        document = get_document(mongo)
        res: Cursor = document.find({"email": email})
        for ans in res:
            atleta = User(**ans)
            if email == atleta.email:
                return atleta
        return None

    def save(self, mongo):
        document = get_document(mongo)
        mydict: dict = self.to_json()
        x = document.insert_one(mydict)
        mydict.pop("_id", None)
        return mydict

    @staticmethod
    def getAll(mongo):
        document = get_document(mongo)
        res: Cursor = document.find({})
        users = []
        for ans in res:
            user = User()
            user.create(**ans)
            users.append(user.to_json())
        return users

    def create(self, name, lastName, ci, fechaNac, telf, genero, pulgar_i, anular_i, medio_i, indice_i, menhique_i, pulgar_d, anular_d, medio_d, indice_d, menhique_d, res_primer_analisis, formula_digital, categ, d10, sqtl, recomendacion1="", recomendacion2="", **args):
        self.name = name
        self.lastName = lastName
        self.ci = ci
        self.fechaNac = fechaNac
        self.telf = telf
        self.genero = genero
        # dedos
        self.pulgar_i = pulgar_i
        self.anular_i = anular_i
        self.medio_i = medio_i
        self.indice_i = indice_i
        self.menhique_i = menhique_i

        self.pulgar_d = pulgar_d
        self.anular_d = anular_d
        self.medio_d = medio_d
        self.indice_d = indice_d
        self.menhique_d = menhique_d
        # res
        self.res_primer_analisis = res_primer_analisis
        self.formula_digital = formula_digital
        self.categ = categ
        self.d10 = d10
        self.sqtl = sqtl
        self.recomendacion1 = recomendacion1
        self.recomendacion2 = recomendacion2

    def __init__(self):
        # self.age = None
        self.name = None
        self.lastName = None
        self.ci = None
        self.fechaNac = None
        self.telf = None
        self.genero = None
        # dedos
        self.pulgar_i = Dedo()
        self.anular_i = Dedo()
        self.medio_i = Dedo()
        self.indice_i = Dedo()
        self.menhique_i = Dedo()

        self.pulgar_d = Dedo()
        self.anular_d = Dedo()
        self.medio_d = Dedo()
        self.indice_d = Dedo()
        self.menhique_d = Dedo()
        # res
        self.res_primer_analisis = None
        self.formula_digital = None
        self.categ = {"arco": 0, "presilla": 0, "verticilo": 0}
        self.d10 = 0
        self.sqtl = 0
        self.recomendacion1 = ""
        self.recomendacion2 = ""

    def print(self):
        print(self.name, "pulgar es:", self.pulgar_i.category)

    def primer_analisis(self):
        dedos = [self.pulgar_i, self.anular_i, self.medio_i, self.indice_i, self.menhique_i, self.pulgar_d,
                 self.anular_d, self.medio_d, self.indice_d, self.menhique_d]
        """
        arco => 1        (A)
        presilla => 2o 3 (L)
        verticillo => 4  (W)
        """
        for dedo in dedos:
            self.categ[dedo.category] += 1
        A = self.categ["arco"]
        L = self.categ["presilla"]
        W = self.categ["verticilo"]

        if (A == 10):
            self.res_primer_analisis = "FUERZA MAXIMA(no incluye potencia)"
            self.formula_digital = "10A"
        if (L >= 6 and W > 0 and A == 0):
            self.res_primer_analisis = "Velocidad, Potencia con un componente de resistencia y coordinacion"
            self.formula_digital = "LW"
        elif (W >= 5 and L > 0 and A == 0):
            self.res_primer_analisis = "Resistencia y Coordinacion de Velocidad y Potencia"
            self.formula_digital = "WL"
        elif (A > 0 and L > 0 and W == 0):
            self.res_primer_analisis = "FUERZA MAXIMA, VELOCIDAD Y POTENCIA"
            self.formula_digital = "AL"
        elif (A > 0 and L > 0 and W > 0):
            # OJO PREGUNTAR
            self.res_primer_analisis = "Depende de la mayor proporcion"
            self.formula_digital = "ALW"
        elif (L == 10):
            self.res_primer_analisis = "POTENCIA Y VELOCIDAD"
            self.formula_digital = "10L"
        elif (W == 10):
            self.res_primer_analisis = "RESISTENCIA Y COORDINACION"
            self.formula_digital = "10W"
        print("primer analisis: ", self.res_primer_analisis)
    
    def remove(mongo, ci):
        document = get_document(mongo)
        document.remove({"ci": ci})


def set_user(user):
    global current_user
    current_user = user


def get_user() -> User:
    global current_user
    return current_user
