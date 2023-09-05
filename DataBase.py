from pymongo import MongoClient
import certifi

URL = 'mongodb+srv://admin:admin@cluster0.wmkww2d.mongodb.net/'

ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(URL, tlsCAFile=ca)
        db = client["BasePoliFligh"] #la base se llamará
        print('Conexion exitosa')
    except ConnectionError:
        print('Error en la conexión con la Base de datos')
    return db