from __main__ import app
from flask import Flask, request, render_template, Response, jsonify, redirect, url_for, session
from werkzeug.utils import secure_filename
from math import log
from mongoengine import connect

from vuelo import Vuelo

import json
from bson.objectid import ObjectId
from bson import json_util
import app as appf


collection_aeropuertos = appf.db['aeropuertos']
collection_vuelos = appf.db['vuelos']
collection_aviones = appf.db['aviones']
collection_clases = appf.db['clases']

def parse_json(data):
    resp = json.loads(json_util.dumps(data))
    resp['_id']=resp['_id']['$oid']
    return resp

@app.route('/consulta-vuelo', methods=['POST', 'GET'])
def consulta():
    if request.method == 'POST':
        try:
            print(session)
            data = request.get_json()
            # print(data)
            origen = data.get('origen')
            destino = data.get('destino')
            fechaVuelo = str(data.get('fechaVuelo'))
            pasajero = data.get('pasajero')
            totalPasajeros: data.get('totalPasajeros')
            fecha=fechaVuelo.split('-')
            fecha.reverse()
            fechaVuelo='-'.join(fecha)
            session['nombre']='Jerson'
            res = collection_vuelos.find({"lugar_origen_id._id":ObjectId(origen), "lugar_destino_id._id":ObjectId(destino), "fecha":fechaVuelo})
            vuelos = [parse_json(aero) for aero in res]
            clases = collection_clases.find()
            clases = [parse_json(clase) for clase in clases]
            adultos_mayores=pasajero['adultos_mayores']
            adultos=pasajero['adultos']
            ninios=pasajero['ninos']
            infantes=pasajero['infantes']
            for vuelo in vuelos:
                precios=[]
                for clase in clases:
                    precio=dict()
                    precio['_id']=clase['_id']
                    precio['nombre']=clase['nombre']
                    asiento=float(clase['precio'])*float(vuelo['distancia_KM'])
                    precio['asiento']=asiento
                    total = adultos_mayores*asiento*0.5 + adultos*asiento + ninios*asiento + infantes*0
                    precio['total']=round(total,2)
                    precios.append(precio)
                vuelo['precios']=precios
                vuelo['asientos_disponibles'] = int(vuelo['id_Avion']['capacidad'])-len(vuelo['listaAsientos'])
            response = jsonify({"result":vuelos})
            response.headers.add('Access-Control-Allow-Headers',
                         "Origin, X-Requested-With, Content-Type, Accept, x-auth")
            return response

        except Exception as e:
            return jsonify({"Error": str(e)}), 500
