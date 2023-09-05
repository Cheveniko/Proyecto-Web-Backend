from DataBase import dbConnection
from bson.objectid import ObjectId

class Avion:
    def __init__(self, modelo, operando, capacidad):
        self.modelo = modelo
        self.operando = operando
        self.capacidad = capacidad

    def update_related_flights(self, id):
        db = dbConnection()
        
        filter = db.aviones.find_one({"_id":ObjectId(id)})

        avion_data = {
            "_id": ObjectId(id),
            "modelo": self.modelo,
            "operando": self.operando,
            "capacidad": self.capacidad            
        }

        res = db.vuelos.update_many({"id_Avion":filter},
                                    {"$set": {"id_Avion": avion_data}})
        return res.modified_count
