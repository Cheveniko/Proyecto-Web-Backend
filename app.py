"""_summary_

    :authors: Jerson Andino, David Mena
    :description: A flask application for test the probabilistic method of information recovery.
"""
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os
from math import log
import time
from mongoengine import connect

#Clases registradas
import DataBase as dbase
from vuelo import Vuelo
from avion import Avion
from clase import Clase
import json
from bson.objectid import ObjectId
from bson import json_util
from aeropuertos import Aeropuertos

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
db = dbase.dbConnection()
app.config['SECRET_KEY'] = b'fL\xabV\x85\x11\x90\x81\x84\xe0\xa7\xf1\xc7\xd5\xf6\xec\x8f\xd1\xc0\xa4\xee)z\xf0'

import avion_views
import clase_views
import aeropuerto_view
import vuelo_view
import consulta_vuelo_view
import reservar_asientos
import reserva_view
import pasajero_view
import boleto_view

from flask_mail import Mail, Message
from datetime import datetime

def parse_json(data):
    return json.loads(json_util.dumps(data))
# RUTAS DE LA APLICACION
reservar_asientos.reservar("asiento1")
@app.route('/', methods=['GET', 'POST'])
def home():
    #Se redirige a cualquier lado, no importa
    # seq=db.sequences.find_one_and_update({"code":"vuelo"},{'$inc': { 'seq': 1 }})
    # print(seq['seq'])
    return "OK",200


app.config['SECRET_KEY'] = "tsfyguaistyatuis589566875623568956"

app.config['MAIL_SERVER'] = "smtp.googlemail.com"

app.config['MAIL_PORT'] = 587

app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = "poliflights@gmail.com"

app.config['MAIL_PASSWORD'] = "bhhcoksaufstncdn"

mail = Mail(app)


@app.route('/send_email', methods=['POST'])
def send_email():

    data = request.get_json()
    msg_title = "Gracias por su compra"
    final = []
    totalFinal = 0


    print(data)
    print(data['infor']['vuelo_id'])

    correo = data['correo']
    cantidad_maleta = 1 # aun falta por llamar del front

    sender = "noreply@app.com"
    msg = Message(msg_title, sender= sender, recipients=[correo]) 
    fecha_actual = datetime.now()
    datas = [data['infor']]
    for infor in datas:
        idVuelo = infor['vuelo_id']

        # for vuelo in vuelos :

        #Organizamos la info de cada pasajero
        pasajeros = infor['pasajeros']
        mayores = pasajeros['adultos_mayores']
        adultos = pasajeros['adultos']
        ninos = pasajeros['ninos']
        infantes = pasajeros['infantes']

        # organizar los precios
        precio_base = round(float(infor['precio_base']),2)

        pMayores = round(len(mayores)*precio_base*0.5,2)
        pAdultos = round(len(adultos)*precio_base,2)
        pNinos = round(len(ninos)*precio_base,2)
        pInfantes = len(infantes)*precio_base*0
        precio_total = round(float(infor['precio_total']),2)
        totalFinal = totalFinal + precio_total
        

        # Hacer la consulta segun el IDvuelo
        response = app.test_client().get(f'/vuelos/{idVuelo}')
        json_content = json.loads(response.get_data(as_text=True))


        # variables para la factura
        ciudad_origen = json_content['Vuelo: ']['lugar_origen_id']['Ciudad']
        ciudad_destino = json_content['Vuelo: ']['lugar_destino_id']['Ciudad']
        numVuelo = json_content['Vuelo: ']['numero_de_vuelo']
        distancia = json_content['Vuelo: ']['distancia_KM']
        fecha = json_content['Vuelo: ']['fecha']
        clase = infor['clase']
        precios ={
            'mayores': pMayores,
            'adultos': pAdultos,
            'ninios': pNinos,
            'infantes': pInfantes,
            'precio_base': precio_base,
            'precio_total': precio_total,
        }

        print("PRECIOS: ",precios)
        dataVuelo = {
            
            'desde': ciudad_origen,
            'hacia': ciudad_destino,
            'vuelo': numVuelo,
            'distancia':distancia, 
            'fecha': fecha,
            'maletas': cantidad_maleta,
            'clase': clase,
        }
        dataVuelo['precios'] = precios
        dataVuelo['mayores'] = mayores
        dataVuelo['adultos'] = adultos
        dataVuelo['ninos'] = ninos
        dataVuelo['infantes'] = infantes
        final.append(dataVuelo)

    iva = totalFinal*0.12
    total = totalFinal + iva
    msg.body = ""

    cabeza = {
        'app_name': "POLI FLIGHTS",
        'title': msg_title,
        'fecha_actual': fecha_actual,
        'subtotal_final': totalFinal,
        'iva': iva,
        'total': total,
    }
    
    msg.html = render_template("email.html",data=final, cabeza=cabeza)
    try:
        mail.send(msg)
        return jsonify({'message': 'Email enviado con Exito!'}), 200
    except Exception as e:
        print(e)
        return f"the email was not sent {e}"
    
if __name__ == '__main__':
    app.run(debug=True)
