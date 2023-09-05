from DataBase import dbConnection
from bson.objectid import ObjectId

class Clase:
    def __init__(self, nombre, precio, descripcion):
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion


    def update_related_flights(self, id):
        db = dbConnection()
        
        origen_filter = db.clases.find_one({"_id":ObjectId(id)})

        clase_data = {
            "_id": ObjectId(id),
            "nombre": self.categoria,
            "precio": self.pasaporte,
            "descripcion": self.nombre           
        }

        if db.boletos.find_one({"codigoClase":origen_filter}):
            res = db.boletos.update_many({"codigoClase":origen_filter},
                                        {"$set": {"codigoClase": clase_data}})
            return res.modified_count
        else:
            return 0
            
    def delete_related_flights(self, id):
        db = dbConnection()
        
        filter = db.clases.find_one({"_id":ObjectId(id)})
        res = db.boletos.delete_many({{"codigoClase":filter}})

        return res.deleted_count