
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from db import app
from werkzeug.exceptions import abort, Response

from Organizacion import Organizacion
from ECOE import ECOE
from Area import Area
from Alarma import Alarma


@app.route('/')
def holaMundo():
    return 'Hola Mundo'

#Rutas de Organizacion
@app.route('/api/v1.0/organizacion/', methods=['GET'])
def muestraOrganizaciones():
    ids = Organizacion().get_organizacion_ids()
    nombres = Organizacion().get_organizacion_nombres()

    return jsonify({"id_organizaciones": ids, "nombres": nombres})

@app.route('/api/v1.0/organizacion/<int:organizacion_id>/', methods=['GET'])
def muestraOrganizacion(organizacion_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        return jsonify({"id_organizacion": organizacion.id_organizacion, "nombre": organizacion.nombre})

    else:
        abort(404)
        # abort(Response("Error"))



@app.route('/api/v1.0/organizacion/', methods=['POST'])
def insertaOrganizacion():
    value = request.json
    nombre = value["nombre"]

    orgIn = Organizacion(nombre)
    orgIn.post_organizacion()

    org = Organizacion().get_ult_organizacion()
    return jsonify({"id" : org.id_organizacion, "nombre" : org.nombre})


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/', methods=['PUT'])
def modificaOrganizacion(organizacion_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        value = request.json
        nombre = value["nombre"]

        organizacion.put_organizacion(nombre)

        return jsonify({"id_organizacion" : organizacion.id_organizacion, "nombre" : organizacion.nombre})
    else:
        abort(404)



@app.route('/api/v1.0/organizacion/<int:organizacion_id>/', methods=['DELETE'])
def eliminaOrganizacion(organizacion_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        organizacion.delete_organizacion()
        return jsonify({"id_organizacion": organizacion.id_organizacion, "nombre": organizacion.nombre})
    else:
        abort(404)


#Rutas de ECOE
@app.route('/api/v1.0/ECOE/', methods=['GET'])
def muestraECOEs():
    ids = ECOE().get_ECOEs_id()
    nombres = ECOE().get_ECOEs_nombres()

    return jsonify({"ids" : ids, "nombres" : nombres})


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/', methods=['GET'])
def muestraECOE(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)
    if(ecoe):
        return jsonify({"id": ecoe.id, "nombre": ecoe.nombre})
    else:
        abort(404)
        #abort(Response("Error"))

@app.route('/api/v1.0/ECOE/', methods=['POST'])
def insertaECOE():
    value = request.json
    nombre = value["nombre"]

    ecoeIn = ECOE(nombre)
    ecoeIn.post_ecoe()

    ecoe = ECOE().get_ult_ecoe()
    return jsonify({"id" : ecoe.id, "nombre" : ecoe.nombre})


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/', methods=['PUT'])
def actualizaECOE(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        value = request.json
        nombre = value["nombre"]

        ecoe.put_ecoe(nombre)
        return jsonify({"id": ecoe.id, "nombre": ecoe.nombre})
    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/', methods=['DELETE'])
def eliminaECOE(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        ecoe.delete_ecoe()
        return jsonify({"id": ecoe.id, "nombre": ecoe.nombre})
    else:
        abort(404)


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

    abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/areas/', methods=['POST'])
def insertaArea(ecoe_id):

    value = request.json
    nombre = value["nombre"]

    areaIn = Area(nombre=nombre, id_ecoe=ecoe_id)
    areaIn.post_area()

    area = Area().get_ult_area()

    return jsonify({"id_area" : area.id_area, "nombre" : area.nombre, "id_ecoe" : area.id_ecoe})


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

    abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/areas/<int:area_id>/', methods=['DELETE'])
def eliminaArea(ecoe_id, area_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    for i in ecoe.areas.all():
        if area_id == i.id_area:
            area = Area().get_area(area_id)
            area.delete_area()
            return jsonify({"id_area": area.id_area, "nombre": area.nombre, "id_ecoe": area.id_ecoe})

    abort(404)


#Rutas de Alumno
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/alumnos/', methods=['GET'])
def muestraAlumnos(ecoe_id):
    return "Hola Mundo"


app.run(port=5000, debug=True)