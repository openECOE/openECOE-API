from db import db
from Cronometro import Cronometro

from db import app
import numpy as np
from flask import jsonify, request
import json
from werkzeug.exceptions import abort, Response

class Estacion(db.Model):
    id_estacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ECOE.id'))
    cronometros = db.relationship('Cronometro', backref='cronometros', lazy='dynamic')

    def __init__(self, nombre='', id_ecoe='', cronometros=[]):
        self.nombre = nombre
        self.id_ecoe = id_ecoe
        #self.grupos = grupos
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

    def existe_estacion_cronometro(self, id_cronometro):
        for cronometro in self.cronometros:
            if(cronometro.id_cronometro==id_cronometro):
                return True
        return False


@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/', methods=['GET'])
def obtenCronometros(estacion_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        cronometros = []
        for cronometro in estacion.cronometros:
            cronometros.append({
                "id_cronometro": cronometro.id_cronometro,
                "nombre": cronometro.nombre,
                "tiempo_total": cronometro.tiempo_total
            })

        return json.dumps(cronometros, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)

@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/<int:cronometro_id>/', methods=['GET'])
def obtenCronometro(estacion_id, cronometro_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        if (estacion.existe_estacion_cronometro(cronometro_id)):
            cronometro = Cronometro().get_cronometro(cronometro_id)
            return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total" : cronometro.tiempo_total})
        else:
            abort(404)

    else:
        abort(404)

@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/', methods=['POST'])
def insertaCronometro(estacion_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        value = request.json
        nombre = value["nombre"]
        tiempo_total = value["tiempo_total"]

        cronometroIn = Cronometro(nombre, tiempo_total, estacion_id)
        cronometroIn.post_cronometro()

        cronometro = Cronometro().get_ult_cronometro()

        return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
    else:
        abort(404)

@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/<int:cronometro_id>/', methods=['PUT'])
def modificaCronometro(estacion_id, cronometro_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        if (estacion.existe_estacion_cronometro(cronometro_id)):
            value = request.json
            nombre = value["nombre"]
            tiempo_total = value["tiempo_total"]
            id_estacion = value["id_estacion"]

            cronometro = Cronometro().get_cronometro(cronometro_id)
            cronometro.put_cronometro(nombre, tiempo_total, id_estacion)

            return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
        else:
            abort(404)

    else:
        abort(404)

@app.route('/api/v1.0/estacion/<int:estacion_id>/cronometros/<int:cronometro_id>/', methods=['DELETE'])
def eliminaCronometro(estacion_id, cronometro_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        if (estacion.existe_estacion_cronometro(cronometro_id)):
            cronometro = Cronometro().get_cronometro(cronometro_id)
            cronometro.delete_cronometro()

            return jsonify({"id_cronometro": cronometro.id_cronometro, "nombre": cronometro.nombre, "tiempo_total": cronometro.tiempo_total})
        else:
            abort(404)

    else:
        abort(404)