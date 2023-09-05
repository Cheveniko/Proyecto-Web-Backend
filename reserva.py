from DataBase import dbConnection
from bson.objectid import ObjectId

class Reserva:
    def __init__(self, codigoClase, capacidadClase):
        # self.numerVuelo =numeroVuelo
        self.codigoClase = codigoClase
        self.capacidadClase = capacidadClase

    def save(self):
        db = dbConnection()
        reserva_data = {
            # "numero_de_vuelo": self.numeroVuelo['seq'],
            "Capacidad_Clase": self.capacidadClase,
            "Codigo_Clase": self.codigoClase,
        }
        db.reservas.insert_one(reserva_data)
