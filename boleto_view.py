from __main__ import app
from flask import Flask, request, render_template, Response, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os
from math import log
import time
from mongoengine import connect

from boleto import Boletos 

import json
from bson.objectid import ObjectId
from bson import json_util
import app as appf

collection_pasajero = appf.db['pasajero']
collection_boleto = appf.db['boletos']
collection_clase = appf.db['clases']



def parse_json(data):
    resp = json.loads(json_util.dumps(data))
    resp['_id']=resp['_id']['$oid']
    return resp


@app.route('/boleto/', methods=['GET', 'POST'])
def boleto():
    if request.method=='POST':
        numeroVuelo = request.form['numeroVuelo']
        numeroAsiento = request.form['numeroAsiento']
        Clase = request.form['codigoClase']
        Pasajero = request.form['codigoPasajero']
        precio = request.form['precio']

        codigoClase = collection_clase.find_one({"_id": ObjectId(Clase)})
        codigoPasajero = collection_pasajero.find_one({"_id": ObjectId(Pasajero)})
        
        if codigoClase:
            if codigoPasajero:
                new_boleto=Boletos(numeroVuelo=numeroVuelo, numeroAsiento=numeroAsiento, codigoClase=codigoClase,codigoPasajero=codigoPasajero,precio=precio)
                new_boleto.save()
                return jsonify({"message":"Boleto registrado exitosamente"})
            else:
                return jsonify({"Message": "NO se ha encontrado el pasajero especificado"})
        else:
            return jsonify({"Message": "NO se ha encontrado la clase especificada"})
        
    if request.method=='GET':
        boletos = [parse_json(clase) for clase in collection_pasajero.find({})]
        return jsonify({"Boletos":boletos})
    

@app.route('/boleto/<id>', methods=['DELETE', 'PUT', 'GET'])
def boletos_id(id):
    if request.method=='DELETE':
        a = collection_boleto.delete_one({"_id":ObjectId(id)})
        code = 404
        if a.deleted_count==1:
            code = 200
        return jsonify({'result':a.deleted_count}), code
    if request.method=='PUT':
        bolet = Boletos(numeroVuelo=request.form['numeroVuelo'], numeroAsiento=request.form['numeroAsiento'], codigoClase=request.form['codigoClase'],codigoPasajero=request.form['codigoPasajero'],precio=request.form['precio'])
        result = collection_boleto.update_one({"_id":ObjectId(id)},{"$set":bolet.__dict__})
        code = 404
        if result.modified_count==1:
            code = 200
        return jsonify({'result':result.modified_count}),code
    if request.method=='GET':
        result = collection_boleto.find_one({"_id":ObjectId(id)})
        code = 404
        if result is not None:
            code=200
            return parse_json(result), code
        return jsonify({"result":None}),code

