from db import db
from Pregunta import Pregunta

from db import app
import numpy as np
from flask import jsonify, request
import json
from werkzeug.exceptions import abort, Response

class Grupo(db.Model):
    id_grupo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    id_estacion = db.Column(db.Integer, db.ForeignKey('estacion.id_estacion'))
    preguntas = db.relationship('Pregunta', backref='preguntas', lazy='dynamic')


    def __init__(self, nombre='', preguntas='', id_estacion=0):
        self.nombre = nombre
        self.preguntas = preguntas
        self.id_estacion = id_estacion

    def get_grupo(self, id):
        grupo = Grupo.query.filter_by(id_grupo=id).first()
        return grupo

    def get_ult_grupo(self):
        grupos = Grupo.query.all()

        numGrupos = len(grupos)
        grupo = grupos[numGrupos-1]

        return grupo


    def post_grupo(self):
        db.session.add(self)
        db.session.commit()

    def put_grupo(self, nombre, id_estacion):
        self.nombre = nombre
        self.id_estacion=id_estacion
        db.session.commit()

    def delete_grupo(self):
        db.session.delete(self)
        db.session.commit()

    def existe_grupo_pregunta(self, id_pregunta):
        for pregunta in self.preguntas:
            if(pregunta.id_pregunta==id_pregunta):
                return True
        return False

@app.route('/api/v1.0/grupos/<int:grupo_id>/pregunta/', methods=['GET'])
def obtenPreguntas(grupo_id):
    grupo = Grupo().get_grupo(grupo_id)

    if (grupo):
        preguntas = []
        for pregunta in grupo.preguntas:
            preguntas.append({
                "id_pregunta" : pregunta.id_pregunta,
                "ref" : pregunta.ref,
                "tipo_pregunta" : pregunta.tipo_pregunta
            })

        return json.dumps(preguntas, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)


@app.route('/api/v1.0/grupos/<int:grupo_id>/pregunta/<int:pregunta_id>/', methods=['GET'])
def obtenPregunta(grupo_id, pregunta_id):
    grupo = Grupo().get_grupo(grupo_id)

    if (grupo):
        if (grupo.existe_grupo_pregunta(pregunta_id)):
            pregunta = Pregunta().get_pregunta(pregunta_id)
            return jsonify({"id_pregunta" : pregunta.id_pregunta, "ref" : pregunta.ref, "tipo_pregunta" : pregunta.tipo_pregunta})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/grupos/<int:grupo_id>/pregunta/', methods=['POST'])
def insertaPregunta(grupo_id):
    grupo = Grupo().get_grupo(grupo_id)

    if (grupo):
        value = request.json
        ref = value["ref"]
        tipo_pregunta = value["tipo_pregunta"]

        preguntaIn = Pregunta(ref, tipo_pregunta, grupo_id)
        preguntaIn.post_pregunta()

        pregunta = Pregunta().get_ult_pregunta()

        return jsonify({"id_pregunta": pregunta.id_pregunta, "ref": pregunta.ref, "tipo_pregunta": pregunta.tipo_pregunta})

    else:
        abort(404)


@app.route('/api/v1.0/grupos/<int:grupo_id>/pregunta/<int:pregunta_id>/', methods=['PUT'])
def modificaPregunta(grupo_id, pregunta_id):
    grupo = Grupo().get_grupo(grupo_id)

    if (grupo):
        if (grupo.existe_grupo_pregunta(pregunta_id)):
            value = request.json
            ref = value["ref"]
            tipo_pregunta = value["tipo_pregunta"]
            id_grupo = value["id_grupo"]

            pregunta = Pregunta().get_pregunta(pregunta_id)
            pregunta.put_pregunta(ref, tipo_pregunta, id_grupo)

            return jsonify({"id_pregunta" : pregunta.id_pregunta, "ref" : pregunta.ref, "tipo_pregunta" : pregunta.tipo_pregunta})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/grupos/<int:grupo_id>/pregunta/<int:pregunta_id>/', methods=['DELETE'])
def eliminaPregunta(grupo_id, pregunta_id):
    grupo = Grupo().get_grupo(grupo_id)

    if (grupo):
        if (grupo.existe_grupo_pregunta(pregunta_id)):
            pregunta = Pregunta().get_pregunta(pregunta_id)
            pregunta.delete_pregunta()

            return jsonify({"id_pregunta": pregunta.id_pregunta, "ref": pregunta.ref, "tipo_pregunta": pregunta.tipo_pregunta})
        else:
            abort(404)

    else:
        abort(404)


