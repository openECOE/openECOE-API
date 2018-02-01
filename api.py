
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from db import app

from Alarma import Alarma
from Area import Area

@app.route('/')
def holaMundo():
    return 'Hola Mundo'

@app.route('/api/v1.0/areas/', methods=['POST'])
def insertaArea():

    value = request.json
    nombre = value["nombre"]

    areaIn = Area(nombre)
    areaIn.post_area()

    area = Area().get_ult_area()

    return jsonify({"id_area" : area.id_area, "nombre" : area.nombre})
   # return area.


@app.route('/api/v1.0/areas/<int:area_id>/', methods=['GET'])
def obtenArea(area_id):
    area = Area().get_area(area_id)
    return jsonify({"id_area" : area.id_area, "nombre" : area.nombre})


@app.route('/api/v1.0/areas/<int:area_id>/', methods=['PUT'])
def modificaArea(area_id):
    value = request.json
    nombre = value["nombre"]

    area = Area().get_area(area_id)
    area.put_area(nombre)

    return jsonify({"id_area": area.id_area, "nombre": area.nombre})


@app.route('/api/v1.0/areas/<int:area_id>/', methods=['DELETE'])
def eliminaArea(area_id):
    area = Area().get_area(area_id)
    area.delete_area()


    return "OK"

app.run(port=5000, debug=True)