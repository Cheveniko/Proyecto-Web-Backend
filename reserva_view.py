from __main__ import app
from flask import Flask, request, render_template, Response, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from math import log
from mongoengine import connect

from reserva import Reserva

import json
from bson.objectid import ObjectId
from bson import json_util
import app as appf

collection_clase = appf.db['clases']
collection_vuelo = appf.db['vuelos']
collection_reserva = appf.db['reserva']

def parse_json(data):
    resp = json.loads(json_util.dumps(data))
    resp['_id']=resp['_id']['$oid']
    return resp

@app.route('/reserva', methods=['POST', 'GET'])
def reserva():

    if request.method == 'POST':
        try:
            data = request.form
            # numero_vuelo = data.get('numero_vuelo')  # Aun por verse
            capacidadClase = data.get('CapacidadClase')
            codigoClase = data.get('codigoClase')
            
            # Buscamos la clase
            claseObj = collection_clase.find_one({"_id": ObjectId(codigoClase)})
            if claseObj:  
                reserva = Reserva(codigoClase = claseObj, capacidadClase = capacidadClase)
                reserva.save()
                return jsonify({"Message: ": "Reserva registrada con exito"})
            else:
                return jsonify({"error:":"Clase especificada no encontrada"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    if request.method == 'GET':
        try:
            res = [parse_json(vuel) for vuel in collection_reserva.find({})]
            return jsonify({"Vuelos":res})

        except Exception as e:
            return jsonify({"error: ": str(e)}), 500

