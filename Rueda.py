from db import db
from db import app

import numpy as np
import json

from werkzeug.exceptions import abort, Response
from flask import jsonify, request

from ECOE import ECOE
from Turno import Turno
from Alumno import Alumno

class Rueda(db.Model):
    id_rueda = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(500))

    # TODO hacer que alumnos sea relationship
    alumnos = db.Column(db.Integer)

    def __init__(self, descripcion, alumnos):
        self.descripcion = descripcion
        self.alumnos = alumnos

    def get_rueda(self, id):
        rueda = Rueda.query.filter_by(id_rueda=id).first()
        return rueda

    def get_ult_rueda(self):
        ruedas = Rueda.query.all()

        numruedas = len(ruedas)
        rueda = ruedas[numruedas-1]

        return rueda

    def post_rueda(self):
        db.session.add(self)
        db.session.commit()

    def put_rueda(self, descripcion):
        self.descripcion = descripcion
        db.session.commit()

    def delete_rueda(self):
        db.session.delete(self)
        db.session.commit()


# RUTAS DE RUEDA
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<string:cod_dia>/turnos/<string:turno_cod>/ruedas/<int:rueda_id>', methods=['GET'])
def muestraRueda(rueda_id):
    rueda = Rueda().get_rueda(rueda_id)

    if(rueda):
        return jsonify({"id_rueda": rueda.id_rueda, "descripcion": rueda.descripcion})

    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<string:cod_dia>/turnos/<string:turno_cod>/ruedas/<int:rueda_id>/alumnos', methods=['GET'])
def obtenAlumnos(rueda_id):
    rueda = Rueda().get_rueda(rueda_id)

    if(rueda):
        alumnos =[]
        for alumno in rueda.alumnos:
            alumnos.append({
                "id_alumno": alumno.id_alumno,
                "Nombre": alumno.nombre,
                "DNI": alumno.dni,
            })

            return json.dump(alumnos, indent=1, ensure_ascii=False).encode('utf8')
        else:
            abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>/turnos/<int:turno_id>/ruedas', methods=['POST'])
def insertaRueda(turno_id):
    turno = Turno().get_turno(turno_id)

    if(turno):
        value = request.json
        descripcion = value["descripcion"]

        ruedaIn = Rueda(descripcion=descripcion, id_turno=turno_id)
        ruedaIn.post_rueda()

        rueda = Rueda().get_ult_rueda()

        return jsonify({"id_rueda":rueda.id_rueda, "descripcion": rueda.descripcion})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>/turnos/<int:turno_id>/ruedas/<int:rueda_id>', methods=['PUT'])
def modificaRueda(rueda_id):
    rueda = Rueda().get_rueda(rueda_id)

    if(rueda):
        value = request.json
        descripcion = value["descripcion"]

        rueda.put_rueda(descripcion)

        return jsonify({"id_rueda": rueda.id_rueda, "descripcion": rueda.descripcion})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>/turnos/<int:turno_id>/ruedas/<int:rueda_id>', methods=['DELETE'])
def eliminaRueda(rueda_id):
    rueda = Rueda().get_rueda(rueda_id)

    if(rueda):
        rueda.delete_rueda()
        return jsonify({"id_rueda": rueda.id_rueda, "descripcion": rueda.descripcion})
    else:
        abort(404)