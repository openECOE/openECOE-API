from db import db
from db import app
import numpy as np
from flask import jsonify, request
import json
from werkzeug.exceptions import abort, Response

from Estacion import Estacion

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

# Relacion Estacion-Grupos
@app.route('/api/v1.0/estacion/<int:estacion_id>/grupos/', methods=['GET'])
def obtenGrupos(estacion_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        grupos = []
        for grupo in estacion.grupos:
            grupos.append({
                "id_grupo": grupo.id_grupo,
                "nombre": grupo.nombre
            })

        return json.dumps(grupos, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)


@app.route('/api/v1.0/estacion/<int:estacion_id>/grupos/<int:grupo_id>/', methods=['GET'])
def obtenGrupo(estacion_id, grupo_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        if (estacion.existe_estacion_grupos()):
            grupo = Grupo().get_grupo(grupo_id)
            return jsonify({"id_grupo": grupo.id_grupo, "nombre": grupo.nombre})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/estacion/<int:estacion_id>/grupos/', methods=['POST'])
def insertaGrupo(estacion_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):

        value = request.json

        if ((not request.json) or (not "nombre" in request.json)):
            abort(400)

        nombre = value["nombre"]

        grupoIn = Grupo(nombre=nombre, id_estacion=estacion_id)
        grupoIn.post_grupo()

        grupo = Grupo().get_ult_grupo()

        return jsonify({"id_grupo": grupo.id_grupo, "nombre": grupo.nombre})

    else:
        abort(404)


@app.route('/api/v1.0/estacion/<int:estacion_id>/grupos/<int:grupo_id>/', methods=['PUT'])
def modificaGrupo(estacion_id, grupo_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        if (estacion.existe_estacion_grupos(grupo_id)):
            value = request.json

            if ((not request.json) or (not "nombre" in request.json) or (not "id_estacion" in request.json)):
                abort(400)

            nombre = value["nombre"]
            id_estacion = value["id_estacion"]

            grupo = Grupo().get_grupo(grupo_id)
            grupo.put_grupo(nombre, id_estacion)

            return jsonify({"id_grupo": grupo.id_grupo, "nombre": grupo.nombre})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/estacion/<int:estacion_id>/grupos/<int:grupo_id>/', methods=['DELETE'])
def eliminaGrupo(estacion_id, grupo_id):
    estacion = Estacion().get_estacion(estacion_id)

    if (estacion):
        if (estacion.existe_estacion_grupos(grupo_id)):
            grupo = Grupo().get_grupo(grupo_id)
            grupo.delete_grupo()

            return jsonify({"id_grupo": grupo.id_grupo, "nombre": grupo.nombre})
        else:
            abort(404)

    else:
        abort(404)



