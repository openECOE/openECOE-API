from db import db
from db import app
import numpy as np
from flask import jsonify, request
import json
from werkzeug.exceptions import abort, Response

from ECOE import ECOE


class Estacion(db.Model):
    id_estacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ECOE.id'))
    grupos = db.relationship('Grupo', backref='grupos', lazy='dynamic')
    cronometros = db.relationship('Cronometro', backref='cronometros', lazy='dynamic')

    def __init__(self, nombre='', id_ecoe='', grupos=[], cronometros=[]):
        self.nombre = nombre
        self.id_ecoe = id_ecoe
        self.grupos = grupos
        self.cronometros = cronometros

    def get_estacion(self, id):
        estacion = Estacion.query.filter_by(id_estacion=id).first()
        return estacion

    def get_ult_estacion(self):
        estaciones = Estacion.query.all()

        numEstacion = len(estaciones)
        estacion = estaciones[numEstacion-1]

        return estacion

    def post_estacion(self):
        db.session.add(self)
        db.session.commit()

    def put_estacion(self, nombre, id_ecoe):
        self.nombre = nombre
        self.id_ecoe = id_ecoe
        db.session.commit()

    def delete_estacion(self):
        db.session.delete(self)
        db.session.commit()

    def existe_estacion_grupos(self, id_grupo):
        for grupo in self.grupos:
            if(grupo.id_grupo==id_grupo):
                return True
        return False

    def existe_estacion_cronometro(self, id_cronometro):
        for cronometro in self.cronometros:
            if(cronometro.id_cronometro==id_cronometro):
                return True
        return False


#Relacion ECOE-Estacion
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estacion/', methods=['GET'])
def obtenEstaciones(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        estaciones = []
        for estacion in ecoe.estaciones:
            estaciones.append({
                "id_estacion" : estacion.id_estacion,
                "nombre" : estacion.nombre
        })

        return json.dumps(estaciones, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estacion/<int:estacion_id>/', methods=['GET'])
def obtenEstacion(ecoe_id, estacion_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        if(ecoe.existe_ecoe_estacion(estacion_id)):
            estacion = Estacion().get_estacion(estacion_id)
            return jsonify({"id_estacion": estacion.id_estacion, "nombre": estacion.nombre})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estacion/', methods=['POST'])
def insertaEstacion(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        value = request.json

        if ((not request.json) or (not "nombre" in request.json)):
            abort(400)

        nombre = value["nombre"]

        estacionIn = Estacion(nombre, ecoe_id)
        estacionIn.post_estacion()

        estacion = Estacion().get_ult_estacion()

        return jsonify({"id_estacion" : estacion.id_estacion, "nombre" : estacion.nombre})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estacion/<int:estacion_id>/', methods=['PUT'])
def modificaEstacion(ecoe_id, estacion_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        if (ecoe.existe_ecoe_estacion(estacion_id)):
            value = request.json

            if ((not request.json) or (not "nombre" in request.json) or (not "id_ecoe" in request.json)):
                abort(400)

            nombre = value["nombre"]
            id_ecoe = value["id_ecoe"]

            estacion = Estacion().get_estacion(estacion_id)
            estacion.put_estacion(nombre, id_ecoe)

            return jsonify({"id_estacion": estacion.id_estacion, "nombre": estacion.nombre, "id_ecoe": estacion.id_ecoe})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estacion/<int:estacion_id>/', methods=['DELETE'])
def eliminaEstacion(ecoe_id, estacion_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        if (ecoe.existe_ecoe_estacion(estacion_id)):
            estacion = Estacion().get_estacion(estacion_id)
            estacion.delete_estacion()

            return jsonify({"id_estacion": estacion.id_estacion, "nombre": estacion.nombre, "id_ecoe": estacion.id_ecoe})
        else:
            abort(404)

    else:
        abort(404)


