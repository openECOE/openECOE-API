
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from db import app

from Alarma import Alarma
from Area import Area
from ECOE import ECOE

@app.route('/')
def holaMundo():
    return 'Hola Mundo'

#Rutas de ECOE
@app.route('/api/v1.0/ECOE/', methods=['POST'])
def insertaECOE():
    value = request.json
    nombre = value["nombre"]

    ecoeIn = ECOE(nombre)
    ecoeIn.post_ecoe()

    ecoe = ECOE().get_ult_ecoe()
    return jsonify({"id" : ecoe.id, "nombre" : ecoe.nombre})


# Rutas de Area, (faltan por insertar los id de las ECOE)
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/areas/', methods=['GET'])
def obtenAreas(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    arrAreasID = []
    arrAreasNombre = []

    for i in ecoe.areas.all():
       arrAreasID.append(i.id_area)
       arrAreasNombre.append(i.nombre)

    return jsonify({"id" : ecoe.id, "nombre" : ecoe.nombre, "id_areas" : arrAreasID, "nombres_areas" : arrAreasNombre})


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/areas/<int:area_id>/', methods=['GET'])
def obtenArea(ecoe_id, area_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    for i in ecoe.areas.all():
        if area_id == i.id_area:
            area = Area().get_area(area_id)
            return jsonify({"id_area": area.id_area, "nombre": area.nombre})

    return "Error"

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/areas/', methods=['POST'])
def insertaArea(ecoe_id):

    value = request.json
    nombre = value["nombre"]

    areaIn = Area(nombre=nombre, id_ecoe=ecoe_id)
    areaIn.post_area()

    area = Area().get_ult_area()

    return jsonify({"id_area" : area.id_area, "nombre" : area.nombre, "id_ecoe" : area.id_ecoe})
    #return "Hola mundo"

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/areas/<int:area_id>/', methods=['PUT'])
def modificaArea(ecoe_id, area_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    value = request.json
    nombre = value["nombre"]

    for i in ecoe.areas.all():
        if area_id == i.id_area:
            area = Area().get_area(area_id)
            area.put_area(nombre)
            return jsonify({"id_area": area.id_area, "nombre": area.nombre})

    return "Error"


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/areas/<int:area_id>/', methods=['DELETE'])
def eliminaArea(ecoe_id, area_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    for i in ecoe.areas.all():
        if area_id == i.id_area:
            area = Area().get_area(area_id)
            area.delete_area()
            return "OK"

    return "Error"

app.run(port=5000, debug=True)