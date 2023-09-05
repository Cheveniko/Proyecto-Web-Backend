from __main__ import app
from flask import Flask, request, render_template, Response, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os
from math import log
import time
from mongoengine import connect

from pasajero import Pasajeros  

import json
from bson.objectid import ObjectId
from bson import json_util
import app as appf

collection_pasajero = appf.db['pasajero']
collection_boleto = appf.db['boletos']


def parse_json(data):
    resp = json.loads(json_util.dumps(data))
    resp['_id']=resp['_id']['$oid']
    return resp


@app.route('/pasajero/', methods=['GET', 'POST'])
def pasajero():
    if request.method=='POST':
        categoria = request.form['categoria']
        pasaporte = request.form['pasaporte']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fechaNacimiento = request.form['fechaNacimiento']

        new_pasajero=Pasajeros(categoria=categoria, pasaporte=pasaporte, nombre=nombre,apellido=apellido, fechaNacimiento=fechaNacimiento)
        new_pasajero.save()
        return jsonify({"message":"Pasajero registrado exitosamente"})
    if request.method=='GET':
        pasajeros = [parse_json(clase) for clase in collection_pasajero.find({})]
        return jsonify({"Pasajeros":pasajeros})

@app.route('/pasajero/<id>', methods=['DELETE', 'PUT', 'GET'])
def pasajero_id(id):
    if request.method=='DELETE':
        a = collection_pasajero.find_one({"_id":ObjectId(id)})
        collection_boleto.delete_many({"codigoPasajero":a})
        result = collection_pasajero.delete_one({"_id":ObjectId(id)})
        code = 404
        if result.deleted_count==1:
            code = 200
        return jsonify({'result':result.deleted_count}), code
    if request.method=='PUT':
        pasa = Pasajeros(categoria=request.form['categoria'], pasaporte=request.form['pasaporte'], nombre=request.form['nombre'],apellido=request.form['apellido'], fechaNacimiento=request.form['fechaNacimiento'])
        av = pasa.update_related_flights(id)
        result = collection_pasajero.update_one({"_id":ObjectId(id)},{"$set":pasa.__dict__})
        code = 404
        if result.modified_count==1:
            code = 200
        return jsonify({'result':result.modified_count}),code
    if request.method=='GET':
        result = collection_pasajero.find_one({"_id":ObjectId(id)})
        code = 404
        if result is not None:
            code=200
            return parse_json(result), code
        return jsonify({"result":None}),code

