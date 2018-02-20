from db import db
from db import app

import numpy as np
import json

from werkzeug.exceptions import abort, Response
from flask import jsonify, request

from Pregunta import Pregunta

class Opcion(db.Model):
    id_opcion = db.Column(db.Integer, primary_key=True)
    puntos = db.Column(db.Integer)
    descripcion = db.Column(db.String(255))

    def __init__(self, puntos, descripcion):
        self.puntos = puntos
        self.descripcion = descripcion

    def get_opcion(self, id):
        opcion = Opcion.query.filter_by(id_opcion=id).first()
        return opcion

    def get_ult_opcion(self):
        opciones = Opcion.query.all()

        numopciones = len(opciones)
        opcion = opciones[numopciones-1]

        return opcion


    def post_opcion(self):
        db.session.add(self)
        db.session.commit()

    def put_opcion(self, puntos, descripcion):
        self.puntos = puntos
        self.descripcion = descripcion
        db.session.commit()

    def delete_opcion(self):
        db.session.delete(self)
        db.session.commit()

#RUTAS DE OPCION
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estaciones/<int:estacion_id>/grupos/<int:grupo_id>/preguntas/<int:pregunta_id>/opciones/<int:opcion_id>', methods=['GET'])
def muestraOpcion(pregunta_id, opcion_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)
    opcion = Opcion().get_opcion(opcion_id)

    if(pregunta):
        return jsonify({"id_opcion": opcion.id_opcion, "puntos": opcion.puntos, "descipcion": opcion.descripcion})

    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estaciones/<int:estacion_id>/grupos/<int:grupo_id>/pregunta/<int:pregunta_id>/opciones', methods=['POST'])
def insertaOpcion(pregunta_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)

    if(pregunta):
        value = request.json
        if ((not request.json) or (not "puntos" in request.json) or (not "descripcion" in request.json)):

            puntos = value["puntos"]
            descripcion = value["descripcion"]

            opcionIn = Opcion(puntos=puntos, descripcion=descripcion)
            opcionIn.post_opcion()

            opcion = Opcion().get_ult_opcion()

        return jsonify({"id_opcion": opcion.id_opcion, "puntos": opcion.puntos, "descipcion": opcion.descripcion})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estaciones/<int:estacion_id>/grupos/<int:grupo_id>/preguntas/<int:pregunta_id>/opciones/<int:opcion_id>', methods=['PUT'])
def modificaOpcion(pregunta_id, opcion_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)
    opcion = Opcion().get_opcion(opcion_id)

    if(pregunta):
        value = request.json
        if ((not request.json) or (not "puntos" in request.json) or (not "descripcion" in request.json)):

            puntos = value["puntos"]
            descripcion = value["descripcion"]

            opcion.put_opcion(puntos, descripcion)

        return jsonify({"id_opcion": opcion.id_opcion, "puntos": opcion.puntos, "descipcion": opcion.descripcion})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estaciones/<int:estacion_id>/grupos/<int:grupo_id>/preguntas/<int:pregunta_id>/opciones/<int:opcion_id>', methods=['DELETE'])
def eliminaOpcion(pregunta_id, opcion_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)
    opcion = Opcion().get_opcion(opcion_id)

    if(opcion):
        opcion.delete_opcion()
        return jsonify({"id_opcion": opcion.id_opcion, "puntos": opcion.puntos, "descipcion": opcion.descripcion})
    else:
        abort(404)