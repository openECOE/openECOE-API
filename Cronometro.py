from db import db
from db import app
import numpy as np
from flask import jsonify, request
import json
from werkzeug.exceptions import abort, Response

from Alarma import Alarma

class Cronometro(db.Model):
    id_cronometro = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    tiempo_total = db.Column(db.Integer)
    id_estacion = db.Column(db.Integer, db.ForeignKey('estacion.id_estacion'))
    alarmas = db.relationship('Alarma', backref='alarmas', lazy='dynamic')

    def __init__(self, nombre='', tiempo_total=0, id_estacion=0):
        self.nombre = nombre
        self.tiempo_total = tiempo_total
        self.id_estacion = id_estacion


        #self.alarmas = alarmas

    def get_cronometro(self, id):
        cronometro = Cronometro.query.filter_by(id_cronometro=id).first()
        return cronometro

    def get_ult_cronometro(self):
        cronometros = Cronometro.query.all()

        numCronometros = len(cronometros)
        cronometro = cronometros[numCronometros - 1]

        return cronometro


    def post_cronometro(self):
        db.session.add(self)
        db.session.commit()

    def put_cronometro(self, nombre, tiempo_total, id_estacion):
        self.nombre = nombre
        self.tiempo_total = tiempo_total
        self.id_estacion = id_estacion
        db.session.commit()


    def delete_cronometro(self):
        db.session.delete(self)
        db.session.commit()

    def existe_cronometro_alarma(self, id_alarma):
        for alarma in self.alarmas:
            if(alarma.id_alarma==id_alarma):
                return True
        return False

@app.route('/api/v1.0/cronometros/<int:cronometro_id>/alarmas/', methods=['GET'])
def obtenAlarmas(cronometro_id):
    cronometro = Cronometro().get_cronometro(cronometro_id)

    if (cronometro):
        alarmas = []
        for alarma in cronometro.alarmas:
            alarmas.append({
                "id_alarma": alarma.id_alarma,
                "tiempo": alarma.tiempo,
                "sonido": alarma.sonido
            })

        return json.dumps(alarmas, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)

@app.route('/api/v1.0/cronometros/<int:cronometro_id>/alarmas/<int:alarma_id>/', methods=['GET'])
def obtenAlarma(cronometro_id, alarma_id):
    cronometro = Cronometro().get_cronometro(cronometro_id)

    if (cronometro):
        if (cronometro.existe_cronometro_alarma(alarma_id)):
            alarma = Alarma().get_alarma(alarma_id)
            return jsonify({"id_alarma": alarma.id_alarma, "tiempo": alarma.tiempo, "sonido": alarma.sonido})
        else:
            abort(404)

    else:
        abort(404)

@app.route('/api/v1.0/cronometros/<int:cronometro_id>/alarmas/', methods=['POST'])
def insertaAlarma(cronometro_id):
    cronometro = Cronometro().get_cronometro(cronometro_id)

    if (cronometro):
        value = request.json
        tiempo = value["tiempo"]
        sonido = value["sonido"]

        alarmaIn = Alarma(tiempo, sonido, cronometro_id)
        alarmaIn.post_alarma()

        alarma = Alarma().get_ult_alarma()

        return jsonify({"id_alarma": alarma.id_alarma, "tiempo": alarma.tiempo, "sonido": alarma.sonido})
    else:
        abort(404)

@app.route('/api/v1.0/cronometros/<int:cronometro_id>/alarmas/<int:alarma_id>/', methods=['PUT'])
def modificaAlarma(cronometro_id, alarma_id):
    cronometro = Cronometro().get_cronometro(cronometro_id)

    if (cronometro):
        if (cronometro.existe_cronometro_alarma(alarma_id)):
            value = request.json
            tiempo = value["tiempo"]
            sonido = value["sonido"]
            id_cronometro = value["id_cronometro"]

            alarma = Alarma().get_alarma(alarma_id)
            alarma.put_alarma(tiempo, sonido, id_cronometro)

            return jsonify({"id_alarma": alarma.id_alarma, "tiempo": alarma.tiempo, "sonido": alarma.sonido})
        else:
            abort(404)

    else:
        abort(404)

@app.route('/api/v1.0/cronometros/<int:cronometro_id>/alarmas/<int:alarma_id>/', methods=['DELETE'])
def eliminaAlarma(cronometro_id, alarma_id):
    cronometro = Cronometro().get_cronometro(cronometro_id)

    if (cronometro):
        if (cronometro.existe_cronometro_alarma(alarma_id)):
            alarma = Alarma().get_alarma(alarma_id)
            alarma.delete_alarma()

            return jsonify({"id_alarma": alarma.id_alarma, "tiempo": alarma.tiempo, "sonido": alarma.sonido})
        else:
            abort(404)

    else:
        abort(404)
