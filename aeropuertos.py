# clase original en la base

from DataBase import dbConnection
from bson.objectid import ObjectId


class Aeropuertos:
    def __init__(self, nombreAeropuerto, Pais,Ciudad):
        self.nombreAeropuerto = nombreAeropuerto
        self.Pais = Pais
        self.Ciudad = Ciudad
        

    def save(self):
        db = dbConnection()
        aeropuerto_data = {
            "nombreAeropuerto": self.nombreAeropuerto,
            "Pais": self.Pais,
            "Ciudad": self.Ciudad            
        }
        db.aeropuertos.insert_one(aeropuerto_data)

    def update_related_flights(self, id):
        db = dbConnection()
        
        origen_filter = db.aeropuertos.find_one({"_id":ObjectId(id)})
        destino_filter = db.aeropuertos.find_one({"_id":ObjectId(id)})

        aeropuerto_data = {
            "_id": ObjectId(id),
            "nombreAeropuerto": self.nombreAeropuerto,
            "Pais": self.Pais,
            "Ciudad": self.Ciudad            
        }

        if origen_filter  == db.vuelos.find_one({"lugar_origen_id":origen_filter})["lugar_origen_id"]:
            res = db.vuelos.update_many({"lugar_origen_id":origen_filter},
                                      {"$set": {"lugar_origen_id": aeropuerto_data}})
            return res.modified_count
        if destino_filter  == db.vuelos.find_one({"lugar_origen_id":origen_filter})["lugar_destino_id"]:
            res = db.vuelos.update_many({"lugar_destino_id":origen_filter},
                                      {"$set": {"lugar_destino_id": aeropuerto_data}})
            return res.modified_count
        
    def delete_related_flights(self, id):
        db = dbConnection()
        
        filter = db.aeropuertos.find_one({"_id":ObjectId(id)})
        res = db.vuelos.delete_many({{"lugar_destino_id":filter}})

        return res.deleted_count
        