from db import db
from db import app
import numpy as np
from flask import jsonify, request
import json
from werkzeug.exceptions import abort, Response

from  Cronometro import Cronometro

class Alarma(db.Model):
    id_alarma = db.Column(db.Integer, primary_key=True)
    tiempo = db.Column(db.Integer)
    sonido = db.Column(db.String(550))
    id_cronometro = db.Column(db.Integer, db.ForeignKey('cronometro.id_cronometro'))

    def __init__(self, tiempo=0, sonido='', id_cronometro=0):
        self.tiempo = tiempo
        self.sonido = sonido
        self.id_cronometro = id_cronometro

    def get_alarma(self, id):
        alarma = Alarma.query.filter_by(id_alarma = id).first()
        return alarma

    def get_ult_alarma(self):
        alarmas = Alarma.query.all()

        numAlarmas = len(alarmas)
        alarma = alarmas[numAlarmas - 1]

        return alarma

    def post_alarma(self):
        db.session.add(self)
        db.session.commit()

    def put_alarma(self, tiempo, sonido, id_cronometro):
        self.tiempo = tiempo
        self.sonido = sonido
        self.id_cronometro = id_cronometro
        db.session.commit()


    def delete_alarma(self):
        db.session.delete(self)
        db.session.commit()

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

        if ((not request.json) or (not "tiempo" in request.json) or (not "sonido" in request.json) or (not "id_cronometro" in request.json)):
            abort(400)

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

            if ((not request.json) or (not "tiempo" in request.json)  or (not "sonido" in request.json) (not "id_cronometro" in request.json)):
                abort(400)

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
