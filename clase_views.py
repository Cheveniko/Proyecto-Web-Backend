from __main__ import app
from flask import Flask, request, render_template, Response, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os
from math import log
import time
from mongoengine import connect

# Clases registradas
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

collection_clases = appf.db["clases"]
collection_boleto = appf.db["boletos"]


def parse_json(data):
    resp = json.loads(json_util.dumps(data))
    resp["_id"] = resp["_id"]["$oid"]
    return resp


@app.route("/clases/", methods=["GET", "POST"])
def clases():
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        descripcion = request.form["descripcion"]
        nueva_clase = Clase(nombre=nombre, precio=precio, descripcion=descripcion)
        response = collection_clases.insert_one(nueva_clase.__dict__)
        return jsonify({"message": "Clase created", "id": f"{response.inserted_id}"})
    if request.method == "GET":
        clases = [parse_json(clase) for clase in collection_clases.find({})]
        return jsonify({"clases": clases})


@app.route("/clases/<id>", methods=["DELETE", "PUT", "GET"])
def clase_id(id):
    if request.method == "DELETE":
        a = collection_clases.find_one({"_id": ObjectId(id)})
        collection_boleto.delete_many({"codigoClase": a})
        result = collection_boleto.delete_one({"_id": ObjectId(id)})
        code = 404
        if result.deleted_count == 1:
            code = 200
        return jsonify({"result": result.deleted_count}), code
    if request.method == "PUT":
        cat = Clase(
            nombre=request.form["nombre"],
            precio=request.form["precio"],
            descripcion=request.form["descripcion"],
        )
        av = cat.update_related_flights(id)
        result = collection_clases.update_one(
            {"_id": ObjectId(id)}, {"$set": cat.__dict__}
        )
        code = 404
        if result.modified_count == 1:
            code = 200
        return jsonify({"result": result.modified_count}), code
    if request.method == "GET":
        result = collection_clases.find_one({"_id": ObjectId(id)})
        code = 404
        if result is not None:
            code = 200
            return parse_json(result), code
        return jsonify({"result": None}), code
