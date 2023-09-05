from DataBase import dbConnection

class Vuelo:
    def __init__(self, id_Avion, lugar_origen_id, lugar_destino_id, fecha, distancia_KM, listaAsientos=None):
        self.numeroVuelo = dbConnection().sequences.find_one_and_update({"code":"vuelo"},{'$inc': { 'seq': 1 }})
        self.id_Avion = id_Avion
        self.lugar_origen_id = lugar_origen_id
        self.lugar_destino_id = lugar_destino_id
        self.fecha = fecha
        self.distancia_KM = distancia_KM
        self.listaAsientos = listaAsientos if listaAsientos else []


    def save(self):
        db = dbConnection()
        vuelo_data = {
            "numero_de_vuelo": self.numeroVuelo['seq'],
            "id_Avion": self.id_Avion,
            "lugar_origen_id": self.lugar_origen_id,
            "lugar_destino_id": self.lugar_destino_id,
            "fecha": self.fecha,
            "distancia_KM": self.distancia_KM,
            "listaAsientos":self.listaAsientos
        }
        db.vuelos.insert_one(vuelo_data)
