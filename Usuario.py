from db import app
from db import db
import numpy as np
from flask import Flask, jsonify, request
from werkzeug.exceptions import abort, Response
from Organizacion import Organizacion

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    apellidos = db.Column(db.String(255))
    id_organizacion = db.Column(db.Integer, db.ForeignKey('organizacion.id_organizacion'))
 #   permisos = db.relationship('Permiso', backref='permisos', lazy='dynamic')

    def __init__(self, nombre='', apellidos='', id_organizacion=0):
        self.nombre = nombre
        self.apellidos = apellidos
        self.id_organizacion = id_organizacion
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


@app.route('/api/v1.0/usuarios/', method=['GET'])
def muestraUsuarios():
    usuarios=[]

    for usuario in Usuario.query.all():
        usuarios.append({
            "id_usuario": usuario.id_usuario,
            "nombre": usuario.nombre,
            "apellidos": usuario.apellidos,
            "id_organizacion": usuario.id_organizacion,

        })
    return jsonify(usuarios)

@app.route('/api/v1.0/usuarios/<int:usuario_id>/', methods=['PUT'])
def actualizaUsuario(usuario_id):
    usuario = Usuario().get_usuario(usuario_id)

    if(usuario):
        value = request.json
        nombre = value["nombre"]
        apellidos = value["apellidos"]

        usuario = Usuario().get_usuario(usuario_id)
        usuario.post_usuario(nombre, apellidos)

        return jsonify({"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos, "id_organizacion": usuario.id_organizacion})
    else:
      abort(404)


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/usuarios/', methods=['GET'])
def muestraUsuarios(organizacion_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        usuarios = []

        for usuario in organizacion.usuarios.all():
            usuarios.append({
                "id_usuario": usuario.id_usuario,
                "nombre": usuario.nombre,
                "apellidos": usuario.apellidos,
                "id_organizacion": usuario.id_organizacion,
            })

        return jsonify(usuarios)
    else:
        abort(404)


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/usuarios/<int:usuario_id>/', methods=['GET'])
def muestraUsuario(organizacion_id, usuario_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        for usuario in organizacion.usuarios.all():
            if usuario_id == usuario.id_usuario:
                usuario = Usuario().get_usuario(usuario_id)
                return jsonify(
                    {"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos,
                     "id_organizacion": usuario.id_organizacion})
        abort(404)
    else:
        abort(404)


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/usuarios/', methods=['POST'])
def insertaUsuario(organizacion_id):
    value = request.json
    nombre = value["nombre"]
    apellidos = value["apellidos"]

    usuarioIn = Usuario(nombre, apellidos, organizacion_id)
    usuarioIn.post_usuario()

    usuario = Usuario().get_ult_usuario()
    return jsonify({"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos" : usuario.apellidos, "id_organizacion" : usuario.id_organizacion})

