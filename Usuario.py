from db import app
from db import db
import numpy as np
from flask import Flask, jsonify, request
from werkzeug.exceptions import abort, Response

import numpy as np
import json

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    apellidos = db.Column(db.String(255))
 #   permisos = db.relationship('Permiso', backref='permisos', lazy='dynamic')

    def __init__(self, nombre='', apellidos='', id_organizacion=0):
        self.nombre = nombre
        self.apellidos = apellidos
        #self.permisos = permisos

    def get_usuario(self, id):
        usuario = Usuario.query.filter_by(id_usuario=id).first()
        return usuario


    def get_ult_usuario(self):
        usuarios = Usuario.query.all()

        numOrg = len(usuarios)
        usuario = usuarios[numOrg - 1]

        return usuario


    def post_usuario(self):
        db.session.add(self)
        db.session.commit()


    def put_usuario(self, nombre, apellidos):
        self.nombre = nombre
        self.apellidos = apellidos
        db.session.commit()


    def delete_usuario(self):
        db.session.delete(self)
        db.session.commit()


@app.route('/api/v1.0/usuarios/', methods=['GET'])
def muestraUsuarios():
    usuarios = []

    for usuario in Usuario.query.all():
        usuarios.append({
            "id_usuario": usuario.id_usuario,
            "nombre": usuario.nombre,
            "apellidos": usuario.apellidos,
        })

    return json.dumps(usuarios, indent=1, ensure_ascii=False).encode('utf8')

@app.route('/api/v1.0/usuarios/<int:usuario_id>/', methods=['GET'])
def muestraUsuario(usuario_id):
    usuario = Usuario().get_usuario(usuario_id)

    return jsonify({"id": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos})

@app.route('/api/v1.0/usuarios/', methods=['POST'])
def insertaUsuario():
    value = request.json

    nombre = value["nombre"]
    apellidos = value["apellidos"]

    usuarioIn = Usuario(nombre, apellidos)
    usuarioIn.post_usuario()

    usuario = Usuario().get_ult_usuario()
    return jsonify({"id": usuario.id_usuario, "nombre": usuario.nombre, "apellidos" : usuario.apellidos})


@app.route('/api/v1.0/usuarios/<int:usuario_id>/', methods=['PUT'])
def actualizaUsuario(usuario_id):
    usuario = Usuario().get_usuario(usuario_id)

    if(usuario):
        value = request.json
        nombre = value["nombre"]
        apellidos = value["apellidos"]

        usuario = Usuario().get_usuario(usuario_id)
        usuario.put_usuario(nombre, apellidos)

        return jsonify({"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos})
    else:
      abort(404)


@app.route('/api/v1.0/usuarios/<int:usuario_id>/', methods=['DELETE'])
def eliminaUsuario(usuario_id):
    usuario = Usuario().get_usuario(usuario_id)

    if (usuario):
        usuario.delete_usuario()
        return jsonify({"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos})
    else:
        abort(404)

