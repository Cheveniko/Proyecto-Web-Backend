from DataBase import dbConnection
from bson.objectid import ObjectId


class Boletos:
    def __init__(self, numeroVuelo,  numeroAsiento, codigoClase, codigoPasajero, precio):
        self.numeroVuelo = numeroVuelo 
        self.numeroAsiento = numeroAsiento
        self.codigoClase = codigoClase
        self.codigoPasajero = codigoPasajero
        self.precio = precio        

    def save(self):
        db = dbConnection()
        boleto_data = {
            "numeroVuelo": self.numeroVuelo,
            "numeroAsiento": self.numeroAsiento,
            "codigoClase": self.codigoClase,
            "codigoPasajero": self.codigoPasajero,
            "precio": self.precio
        }
        db.boletos.insert_one(boleto_data)