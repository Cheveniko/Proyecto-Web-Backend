from __main__ import app
from flask import Flask, request, render_template, Response, jsonify, redirect, url_for
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os
from math import log
import time
from mongoengine import connect

#Clases registradas
import json
from bson.objectid import ObjectId
from bson import json_util
from aeropuertos import Aeropuertos
import app as appf

collection_aeropuertos = appf.db['aeropuertos']
collection_vuelos = appf.db['vuelos']

def parse_json(data):
    resp = json.loads(json_util.dumps(data))
    resp['_id']=resp['_id']['$oid']
    return resp

@app.route('/aeropuertos', methods=['POST', 'GET'])
@cross_origin()
def ADD_aeropuerto():
    if request.method=='POST':
        try:
            data = request.form
            nombre_aeropuerto = data.get('nombreAeropuerto')
            pais = data.get('Pais')  
            ciudad = data.get('Ciudad')
            aeropuerto = Aeropuertos(nombreAeropuerto=nombre_aeropuerto, Ciudad=ciudad, Pais=pais)
            aeropuerto.save()
            return jsonify({"mensaje": "Aeropuerto agregado correctamente"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    if request.method=='GET':
        aeropuertos = [parse_json(aero) for aero in collection_aeropuertos.find({})]
        return jsonify({"Aeropuertos":aeropuertos})

@app.route('/aeropuertos/<id>', methods=['DELETE', 'PUT', 'GET'])
def aeropuertos_id(id):
    if request.method=='DELETE':
        
        filter = collection_aeropuertos.find_one({"_id":ObjectId(id)})
        print(filter)
        collection_vuelos.delete_many({"lugar_origen_id":filter})
        collection_vuelos.delete_many({"lugar_destino_id":filter})
        result = collection_aeropuertos.delete_one({"_id":ObjectId(id)})
        code = 404
        if result.deleted_count==1:
            code = 200     
        return jsonify({'result':result.deleted_count}), code
    if request.method=='PUT':
        aero = Aeropuertos(nombreAeropuerto=request.form['nombreAeropuerto'],Pais=request.form['Pais'],Ciudad=request.form['Ciudad'])
        vue = aero.update_related_flights(id)
        code = 404
        if vue > 1:
            result = collection_aeropuertos.update_one({"_id":ObjectId(id)},{"$set":aero.__dict__})
            if result.modified_count==1:
                code = 200
            return jsonify({'result':result.modified_count}),code
        return jsonify({'resultVuelo':vue}),code
    if request.method=='GET':
        result = collection_aeropuertos.find_one({"_id":ObjectId(id)})
        code = 404
        if result is not None:
            code=200
            return parse_json(result), code
        return jsonify({"result":None}),code
    



