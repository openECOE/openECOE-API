from db import db
from db import app

import numpy as np
import json

from werkzeug.exceptions import abort, Response
from flask import jsonify, request


class Dia(db.Model):
    id_dia = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Integer)
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ECOE.id'))


    #turnos = db.Column(db.Integer)


    def __init__(self, fecha, turnos):
        self.fecha = fecha
        self.turnos = turnos

    def get_dia(self, id):
        dia = Dia.query.filter_by(id_dia=id).first()
        return dia

    def get_ult_dia(self):
        dias = Dia.query.all()

        numdias = len(dias)
        dia = dias[numdias-1]

        return dia

    def post_dia(self):
        db.session.add(self)
        db.session.commit()

    def put_dia(self, fecha):
        self.fecha = fecha
        db.session.commit()

    def delete_dia(self):
        db.session.delete(self)
        db.session.commit()

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>/turnos', methods=['GET'])
def obtenTurnos(dia_id):
    dia = Dia().get_dia(dia_id)

    if(dia):
        turnos =[]
        for turno in dia.turnos:
            turnos.append({
                "id_turno": turno.id_turno,
                "hora inicio": turno.hora_inicio,
            })

            return json.dump(turnos, indent=1, ensure_ascii=False).encode('utf8')
        else:
            abort(404)