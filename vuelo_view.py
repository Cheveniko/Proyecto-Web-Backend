from __main__ import app
from flask import Flask, request, render_template, Response, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os
from math import log
import time
from mongoengine import connect

from vuelo import Vuelo

import json
from bson.objectid import ObjectId
from bson import json_util
import app as appf


#En caso de no existir la coleccion lugares
collection_lugares = appf.db["lugares"]
collection_aviones = appf.db['aviones']
collection_clases = appf.db['clases']
collection_aeropuertos = appf.db['aeropuertos']
collection_vuelos = appf.db['vuelos']


def parse_json(data):
    resp = json.loads(json_util.dumps(data))
    resp['_id']=resp['_id']['$oid']
    return resp

@app.route('/vuelo', methods=['POST', 'GET'])
def vuelo():

    if request.method == 'POST':
        try:
            data = request.form
            numero_vuelo = data.get('numero_vuelo')  # Aun por verse
            id_Avion = data.get('id_Avion')
            lugar_origen_id = data.get('lugar_origen_id')
            lugar_destino_id = data.get('lugar_destino_id')
            fecha = data.get('fecha')
            distancia_KM = data.get('distancia_KM')
            listaAsientos = data.get('asientos')

            # Buscar el avion, origen y aeropuerto aeropuerto por su ID
            avion = collection_aviones.find_one({"_id": ObjectId(id_Avion)})
            origen = collection_aeropuertos.find_one({"_id": ObjectId(lugar_origen_id)})
            destino = collection_aeropuertos.find_one({"_id": ObjectId(lugar_destino_id)})


            if avion:
                if origen:
                    if destino:
                        # Crear un nuevo aeropuerto relacionado con el lugar
                        vuelo = Vuelo(id_Avion=avion, lugar_origen_id=origen, 
                                lugar_destino_id=destino, fecha=fecha, distancia_KM=distancia_KM)
                        vuelo.save()
                        return jsonify({"mensaje": "Vuelo agregado correctamente"}), 200
                    else:
                        return jsonify({"error": "El destino especificado no existe"}), 404
                else:
                    return jsonify({"error": "El origen especificado no existe"}), 404
            else:
                return jsonify({"error": "El avion especificado no existe"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    if request.method == 'GET':
        vuelos = [parse_json(vuel) for vuel in collection_vuelos.find({})]
        return jsonify({"Vuelos":vuelos})
    
@app.route('/vuelo/<id>', methods=['DELETE', 'PUT', 'GET'])
def eliminar_vuelo(id):
    if request.method == 'DELETE':
        try:
            # Intenta eliminar el vuelo por su ID
            resultado = collection_vuelos.delete_one({"_id": ObjectId(id)})
            if resultado.deleted_count > 0:
                return jsonify({"mensaje": "Vuelo eliminado correctamente"}), 200
            else:
                return jsonify({"error": "Vuelo no encontrado"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    if request.method == 'PUT':
        try:

            data = request.form
            id_Avion = data.get('id_Avion')
            lugar_origen_id = data.get('lugar_origen_id')
            lugar_destino_id = data.get('lugar_destino_id')
            fecha = data.get('fecha')
            distancia_KM = data.get('distancia_KM')

            vuelo = collection_vuelos.find_one({"_id": ObjectId(id)})
            if vuelo:
                vuelo['id_Avion'] = collection_aviones.find_one({"_id":ObjectId(id_Avion)})
                vuelo['lugar_origen_id'] = collection_aeropuertos.find_one({"_id":ObjectId(lugar_origen_id)})
                vuelo['lugar_destino_id'] = collection_aeropuertos.find_one({"_id":ObjectId(lugar_destino_id)})
                vuelo['fecha'] = fecha
                vuelo['distancia_KM'] = distancia_KM
                
                collection_vuelos.replace_one({"_id": ObjectId(id)}, vuelo)
                
                return jsonify({"mensaje": "Vuelo actualizado correctamente"}), 200
            else:
                return jsonify({"error": "El vuelo especificado no existe"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    

@app.route('/vuelos/<id>', methods=['GET'])
def get_vuelo_clase(id):    
    # if request.method=='GET':
    #     try:
    #         # vuelo = collection_vuelos.find_one({'numero_de_vuelo':numVuelo})
    #         num_vuelo = info.split('-')[0]
    #         clase_id = info.split('-')[1]
    #         print(num_vuelo)
    #         print(clase_id)
    #         vuelo = collection_vuelos.find_one({"numero_de_vuelo":num_vuelo})
    #         clase = collection_clases.find_one({"_id":ObjectId(clase_id)})
    #         print(vuelo)
    #         print(clase)
    #         return "OK",200
    #     except Exception as e:
    #         print(e)
        
    if request.method == 'GET':
        try:
            vuelo = collection_vuelos.find_one({"_id": ObjectId(id)})
            return jsonify({"Vuelo: ": parse_json(vuelo)})
        except Exception as e:
            return jsonify({"error: ": str(e)})

@app.route('/asiento/<id>', methods=['PUT'])
def registrarAsiento(id):    

    try:
        data = request.form
        num_asiento = data.get('numAsiento')
        if num_asiento is None: 
            return jsonify({'error': 'Proporciona un número de asiento válido'}), 400
        
        reserva = collection_vuelos.find_one({'_id': ObjectId(id)})
        print(reserva)
        if reserva is None:
            return jsonify({'error': 'Reserva no encontrada'}), 404

        asientos_actuales = reserva.get('listaAsientos', [])

        # Filtrar y eliminar valores 'null' (None) de la lista
        asientos_actuales = [a for a in asientos_actuales if a is not None]
        asientos_actuales.append(num_asiento)

        collection_vuelos.update_one({'_id': ObjectId(id)}, {'$set': {'listaAsientos': asientos_actuales}})

        return jsonify({'message': 'Asiento registrado exitosamente'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

# Para limpiar todos los asientos del vuelo, id del vuelo
@app.route('/asiento/<id>', methods=['DELETE'])
def limpiar_asientos(id):
    reserva = collection_vuelos.find_one({'_id': ObjectId(id)})
    if reserva is None:
        return jsonify({'error': 'Reserva no encontrada'}), 404
    
    collection_vuelos.update_one({'_id': ObjectId(id)}, {'$set': {'listaAsientos': []}})
    
    return jsonify({'message': 'Array de asientos limpiado exitosamente'}), 200
    
# Para limpiar todos los asientos del vuelo, id del vuelo    
@app.route('/eliminarAsiento/<id>', methods=['PUT'])
def limpiar_asiento(id):
    try:
        data = request.form
        num_asiento_eliminar = data.get('numAsiento')
        if num_asiento_eliminar is None:
            return jsonify({'error': 'Proporciona un número de asiento a eliminar válido'}), 400
        reserva = collection_vuelos.find_one({'_id': ObjectId(id)})
        if reserva is None:
            return jsonify({'error': 'Reserva no encontrada'}), 404
        asientos_actuales = reserva.get('listaAsientos', [])

        if num_asiento_eliminar in asientos_actuales:
            asientos_actuales.remove(num_asiento_eliminar)
            collection_vuelos.update_one({'_id': ObjectId(id)}, {'$set': {'listaAsientos': asientos_actuales}})
            return jsonify({'message': 'Asiento eliminado exitosamente'}), 200
        else:
            return jsonify({'error': 'El número de asiento no está en la lista'}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

