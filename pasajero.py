from DataBase import dbConnection
from bson.objectid import ObjectId


class Pasajeros:
    def __init__(self, categoria, pasaporte,nombre, apellido, fechaNacimiento):
        self.categoria = categoria
        self.pasaporte = pasaporte
        self.nombre = nombre
        self.apellido = apellido
        self.fechaNacimiento = fechaNacimiento
        

    def save(self):
        db = dbConnection()
        pasajero_data = {
            "categoria": self.categoria,
            "pasaporte": self.pasaporte,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fechaNacimiento": self.fechaNacimiento            
        }
        db.pasajero.insert_one(pasajero_data)

    def update_related_flights(self, id):
        db = dbConnection()
        
        origen_filter = db.pasajero.find_one({"_id":ObjectId(id)})

        pasajero_data = {
            "_id": ObjectId(id),
            "categoria": self.categoria,
            "pasaporte": self.pasaporte,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fechaNacimiento": self.fechaNacimiento            
        }

        if db.boletos.find_one({"codigoPasajero":origen_filter}):
            res = db.boletos.update_many({"codigoPasajero":origen_filter},
                                      {"$set": {"codigoPasajero": pasajero_data}})
            return res.modified_count
        else:
            return 0
        
    def delete_related_flights(self, id):
        db = dbConnection()
        
        filter = db.pasajero.find_one({"_id":ObjectId(id)})
        res = db.boletos.delete_many({{"codigoPasajero":filter}})

        return res.deleted_count