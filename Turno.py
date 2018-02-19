from db import db
from db import app

import numpy as np
import json

from werkzeug.exceptions import abort, Response
from flask import jsonify, request

from Dia import Dia

class Turno(db.Model):
    id_turno = db.Column(db.Integer, primary_key=True)
    hora_inicio = db.Column(db.Integer)

    # TODO hacer que ruedas sea relationship
    ruedas = db.Column(db.Integer)

    def __init__(self, hora_inicio, ruedas):
        self.hora_inicio = hora_inicio
        self.ruedas = ruedas

    def get_turno(self, id):
        turno = Turno.query.filter_by(id_turno = id).first()
        return turno

    def get_ult_turno(self):
        turnos = Turno.query.all()

        numturnos = len(turnos)
        turno = turnos[numturnos-1]

        return turno

    def post_turno(self):
        db.session.add(self)
        db.session.commit()

    def put_turno(self, hora_inicio):
        self.hora_inicio = hora_inicio
        db.session.commit()


    def delete_turno(self):
        db.session.delete(self)
        db.session.commit()

# RUTAS DE TURNO
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>/turnos/<int:turno_id>', methods=['GET'])
def muestraTurno(dia_id, turno_id):
    dia = Dia().get_dia(dia_id)
    turno = Turno().get_turno(turno_id)


    if(dia):
        return jsonify({"id_turno": turno.id_turno, "hora_inicio": turno.hora_inicio})

    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>/turnos/<int:turno_id>/ruedas', methods=['GET'])
def obtenRuedas(turno_id):
    turno = Turno().get_turno(turno_id)

    if(turno):
        ruedas =[]
        for rueda in turno.ruedas:
            ruedas.append({
                "id_ruedas": rueda.id_rueda,
                "descripción": rueda.descripcion,
            })

            return json.dump(ruedas, indent=1, ensure_ascii=False).encode('utf8')
        else:
            abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>/turnos', methods=['POST'])
def insertaTurno(dia_id):
    dia = Dia().get_dia(dia_id)

    if(dia):
        value = request.json
        if ((not request.json) or (not "hora_inicio" in request.json)):

            hora_inicio = value["hora_inicio"]

            turnoIn = Turno(hora_inicio=hora_inicio, id_dia=dia_id)
            turnoIn.post_turno()

            turno = Turno().get_ult_turno()

        return jsonify({"id_turno": turno.id_turno, "hora_inicio": turno.hora_inicio})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id/dias/int:dia_id>/turnos/<int:turno_id>', methods=['PUT'])
def modificaTurno(dia_id, turno_id):
    dia = Dia().get_dia(dia_id)
    turno = Turno().get_turno(turno_id)

    if(dia):
        value = request.json
        if ((not request.json) or (not "hora_inicio" in request.json)):

            hora_inicio = value["hora_inicio"]

            turno.put_turno(hora_inicio)

        return jsonify({"id_turno": turno.id_turno, "hora_inicio": turno.hora_inicio})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>/turnos/<int:turno_id>', methods=['DELETE'])
def eliminaTurno(dia_id, turno_id):
    dia = Dia().get_dia(dia_id)
    turno = Turno().get_turno(turno_id)

    if(dia):
        turno.delete_turno()
        return jsonify({"id_turno": turno.id_turno, "hora_inicio": turno.hora_inicio})
    else:
        abort(404)