from __main__ import app
from flask import Flask, request, render_template, Response, jsonify, redirect, url_for
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
import app as appf

# db = dbase.dbConnection()
collection_aviones=appf.db['aviones']
collection_vuelos=appf.db['vuelos']

def parse_json(data):
    return json.loads(json_util.dumps(data))

@app.route('/aviones/', methods=['GET', 'POST'])
def aviones():
    if request.method=='POST':
        modelo = request.form['modelo']
        operando = request.form['operando']
        capacidad = request.form['capacidad']
        nuevo_avion=Avion(modelo=modelo,operando=operando,capacidad=capacidad)
        response = collection_aviones.insert_one(nuevo_avion.__dict__)
        return jsonify({"message":"Avion created","id": f"{response.inserted_id}"})
    if request.method=='GET':
        aviones = [parse_json(avion) for avion in collection_aviones.find({})]
        return jsonify({"aviones":aviones})

@app.route('/aviones/<id>', methods=['DELETE', 'PUT', 'GET'])
def aviones_id(id):
    if request.method=='DELETE':
        a = collection_aviones.find_one({"_id":ObjectId(id)})
        collection_vuelos.delete_many({"id_Avion":a})
        result = collection_aviones.delete_one({"_id":ObjectId(id)})
        code = 404
        if result.deleted_count==1:
            code = 200
        return jsonify({'result':result.deleted_count}), code
    if request.method=='PUT':
        avion = Avion(modelo=request.form['modelo'],operando=request.form['operando'],capacidad=request.form['capacidad'])
        av = avion.update_related_flights(id)
        result = collection_aviones.update_one({"_id":ObjectId(id)},{"$set":avion.__dict__})
        code = 404
        if result.modified_count==1:
            code = 200
        return jsonify({'result':result.modified_count}),code
    if request.method=='GET':
        result = collection_aviones.find_one({"_id":ObjectId(id)})
        code = 404
        if result is not None:
            code=200
            return parse_json(result), code
        return jsonify({"result":None}),code