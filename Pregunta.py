from db import db
from db import app

import numpy as np
import json

from werkzeug.exceptions import abort, Response
from flask import jsonify, request

from Grupo import Grupo

class Pregunta(db.Model):
    id_pregunta = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.String(255))
    tipo_opcion = db.Column(db.Integer)

    # TODO hacer que area y opcion sea relationship
    area_pregunta = db.Column(db.Integer)
    opciones = db.Column(db.Integer)

    def __init__(self, referencia, tipo_opcion, area_pregunta, opciones):
        self.referencia = referencia
        self.tipo_opcion = tipo_opcion
        self.area_pregunta = area_pregunta
        self.opciones = opciones

    def get_pregunta(self, id):
        pregunta = Pregunta.query.filter_by(id_pregunta=id).first()
        return pregunta

    def get_ult_pregunta(self):
        preguntas = Pregunta.query.all()

        numpreguntas = len(preguntas)
        pregunta = preguntas[numpreguntas-1]

        return pregunta

    def post_pregunta(self):
        db.session.add(self)
        db.session.commit()

    def put_pregunta(self, ref, tipo_opcion, area_pregunta):
        self.ref = ref
        self.tipo_opcion = tipo_opcion
        self.area_pregunta = area_pregunta

        db.session.commit()

    def delete_pregunta(self):
        db.session.delete(self)
        db.session.commit()

#RUTAS DE PREGUNTA
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estaciones/<int:estacion_id>/grupos/<string:grupo_nombre>/preguntas/<int:pregunta_id>', methods=['GET'])
def muestraPregunta(pregunta_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)

    if(pregunta):
        return jsonify({"id_pregunta": pregunta.id_pregunta, "tipo_opcion": pregunta.tipo_opcion, "area_pregunta": pregunta.area_pregunta})

    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estaciones/<int:estacion_id>/grupos/<string:grupo_nombre>/preguntas/<int:pregunta_id>/opciones', methods=['GET'])
def obtenOpciones(pregunta_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)

    if(pregunta):
        opciones = []
        for opcion in pregunta.opciones:
            opciones.append({
                "id_opcion": opcion.id_opcion,
                "puntos": opcion.puntos,
                "descripcion": opcion.descripcion,
            })

            return json.dump(opciones, indent=1, ensure_ascii=False).encode('utf8')
        else:
            abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estaciones/<int:estacion_id>/grupos/<int:grupo_id>/preguntas', methods=['POST'])
def insertaPregunta(grupo_id):
    grupo = Grupo().get_grupo(grupo_id)

    if(grupo):
        value = request.json
        ref = value["ref"]
        tipo_opcion = value["tipo_opcion"]
        area_pregunta = value["area_pregunta"]

        preguntaIn = Pregunta(ref=ref, tipo_opcion=tipo_opcion, area_pregunta=area_pregunta)
        preguntaIn.post_pregunta()

        pregunta = Pregunta.get_ult_pregunta()

        return jsonify({"id_pregunta": pregunta.id_pregunta, "ref": pregunta.ref, "tipo_opcion": pregunta.tipo_opcion, "area_pregunta": pregunta.area_pregunta})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estaciones/<int:estacion_id>/grupos/<int:grupo_id>/preguntas/<int:pregunta_id>', methods=['PUT'])
def modificaPregunta(pregunta_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)

    if(pregunta):
        value = request.json
        ref = value["ref"]
        tipo_opcion = value["tipo_opcion"]
        area_pregunta = value["area_pregunta"]

        pregunta.put_pregunta(ref, tipo_opcion, area_pregunta)

        return jsonify({"id_pregunta": pregunta.id_pregunta, "ref": pregunta.ref, "tipo_opcion": pregunta.tipo_opcion, "area_pregunta": pregunta.area_pregunta})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estaciones/<int:estacion_id>/grupos/<int:grupo_id>/preguntas/<int:pregunta_id>', methods=['DELETE'])
def eliminaPregunta(pregunta_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)

    if(pregunta):
        pregunta.delete_pregunta()
        return jsonify({"id_pregunta": pregunta.id_pregunta, "ref": pregunta.ref, "tipo_opcion": pregunta.tipo_opcion, "area_pregunta": pregunta.area_pregunta})
    else:
        abort(404)


