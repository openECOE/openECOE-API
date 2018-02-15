from db import app
from db import db
import numpy as np
from flask import Flask, jsonify, request
from werkzeug.exceptions import abort, Response

import numpy as np
import json


class Permiso(db.Model):
    id_permiso = db.Column(db.Integer, primary_key=True)
    id_tipoPermiso = db.Column(db.Integer)
    id_organizacion = db.Column(db.Integer)
    id_ecoe = db.Column(db.Integer)
    id_estacion = db.Column(db.Integer)

    def __init__(self, id_tipoPermiso, id_organizacion, id_ecoe, id_estacion):
        self.id_tipoPermiso = id_tipoPermiso
        self.id_organizacion = id_organizacion
        self.id_ecoe = id_ecoe
        self.id_estacion = id_estacion

    def get_permiso(self, id):
        permiso = Permiso.query.filter_by(id_permiso=id).first()
        return permiso

    def get_ult_permiso(self):
        permisos = Permiso.query.all()

        numPerm = len(permisos)
        permiso = permisos[numPerm - 1]

        return permiso

    def post_permiso(self):
        db.session.add(self)
        db.session.commit()



    #Edita el tipo de permiso.
    def put_permiso(self, id_tipoPermiso, id_organizacion, id_ecoe, id_estacion):
        self.id_tipoPermiso = id_tipoPermiso
        self.id_organizacion = id_organizacion
        self.id_ecoe = id_ecoe
        self.id_estacion = id_estacion

        db.session.commit()


    def delete_permiso(self):
        db.session.delete(self)
        db.session.commit()

@app.route('/api/v1.0/permisos/', methods=['GET'])
def muestraPermisos():
    permisos = []

    for permiso in Permiso.query.all():
        permisos.append({
            "id_permiso": permiso.id_tipoPermiso,
            "id_tipoPermiso": permiso.id_tipoPermiso,
            "id_organizacion": permiso.id_organizacion,
            "id_ecoe": permiso.id_ecoe,
            "id_estacion": permiso.id_estacion
        })

    return json.dumps(permisos, indent=1, ensure_ascii=False).encode('utf8')

@app.route('/api/v1.0/permisos/<int:permiso_id>/', methods=['GET'])
def muestraPermiso(permiso_id):
    permiso = Permiso().get_permiso(permiso_id)

    if(permiso):
        return jsonify({"id_permiso": permiso.id_permiso, "id_tipoPermiso": permiso.id_tipoPermiso, "id_organizacion": permiso.id_organizacion, "id_ecoe": permiso.id_ecoe, "id_estacion": permiso.id_estacion})
    else:
        abort(404)

@app.route('/api/v1.0/permisos/', methods=['POST'])
def insertaPermiso():
    value = request.json

    id_tipoPermiso = value["id_tipoPermiso"]
    id_organizacion = value["id_organizacion"]
    id_ecoe = value["id_ecoe"]
    id_estacion = value["id_estacion"]

    permisoIn = Permiso(id_tipoPermiso, id_organizacion, id_ecoe, id_estacion)
    permisoIn.post_permiso()

    permiso = Permiso().get_ult_per()
    return jsonify({"id_permiso": permiso.id_permiso, "id_tipoPermiso": permiso.id_tipoPermiso, "id_organizacion": permiso.id_organizacion, "id_ecoe": permiso.id_ecoe, "id_estacion": permiso.id_estacion})


@app.route('/api/v1.0/permisos/<int:permiso_id>/', methods=['PUT'])
def actualizaPermiso(permiso_id):
    permiso = Permiso().get_usuario(permiso_id)

    if(permiso):
        value = request.json

        id_tipoPermiso = value["id_tipoPermiso"]
        id_organizacion = value["id_organizacion"]
        id_ecoe = value["id_ecoe"]
        id_estacion = value["id_estacion"]

        permiso = Permiso().get_permiso(permiso_id)
        permiso.put_permiso()
        permiso.put_permiso(id_tipoPermiso, id_organizacion, id_ecoe, id_estacion)

        return jsonify({"id_permiso": permiso.id_permiso, "id_tipoPermiso": permiso.id_tipoPermiso, "id_organizacion": permiso.id_organizacion, "id_ecoe": permiso.id_ecoe, "id_estacion": permiso.id_estacion})
    else:
        abort(404)


@app.route('/api/v1.0/permisos/<int:permiso_id>/', methods=['DELETE'])
def eliminaPermiso(permiso_id):
    permiso = Permiso().get_permiso(permiso_id)

    if (permiso):
        permiso.delete_usuario()
        return jsonify({"id_permiso": permiso.id_permiso, "id_tipoPermiso": permiso.id_tipoPermiso, "id_organizacion": permiso.id_organizacion, "id_ecoe": permiso.id_ecoe, "id_estacion": permiso.id_estacion})
    else:
        abort(404)

