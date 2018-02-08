from db import db
from db import app

import numpy as np
import json

from werkzeug.exceptions import abort, Response
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from Usuario import Usuario

OrgUsu = db.Table('OrgUsu', db.Column('id_organizacion', db.Integer, db.ForeignKey('organizacion.id_organizacion'), primary_key=True), db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id_usuario'), primary_key=True))


class Organizacion(db.Model):
    id_organizacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    usuarios = db.relationship('Usuario', secondary=OrgUsu, lazy ='subquery', backref=db.backref('usuarios', lazy = 'dynamic'))
    #ecoes = db.relationship('ECOE', backref='ecoes', lazy='dynamic')

    def __init__(self, nombre='', usuarios=[]):
        self.nombre = nombre
        self.usuarios = usuarios
       # self.ecoes = ecoes

    def get_organizacion_ids(self):
        ids = Organizacion.query.with_entities(Organizacion.id_organizacion).all()
        return list(np.squeeze(ids))

    def get_organizacion_nombres(self):
        nombres = Organizacion.query.with_entities(Organizacion.nombre).all()
        return list(np.squeeze(nombres))

    def get_organizacion(self, id):
        organizacion = Organizacion.query.filter_by(id_organizacion=id).first()
        return organizacion

    def get_ult_organizacion(self):
        organizaciones = Organizacion.query.all()

        numOrg = len(organizaciones)
        organizacion = organizaciones[numOrg - 1]

        return organizacion

    def post_organizacion(self):
        db.session.add(self)
        db.session.commit()


    def put_organizacion(self, nombre):
        self.nombre = nombre
        db.session.commit()

    def delete_organizacion(self):
        db.session.delete(self)
        db.session.commit()

    def existe_organizacion_usuario(self, id_usuario):
        for usuario in self.usuarios:
            if(usuario.id_usuario==id_usuario):
                return True
        return False


    def put_organizacion_usuario(self, usuario):
        self.usuarios.append(usuario)
        db.session.commit()

    def delete_organizacion_usuario(self, usuario):
        self.usuarios.remove(usuario)
        db.session.commit()

    def get_usuario_organizaciones(self, usuario_id):

        ids = db.session.query(OrgUsu).filter_by(id_usuario=usuario_id)
        organizaciones=[]

        for id in ids:
            organizaciones.append(Organizacion().get_organizacion(id.id_organizacion))

        return organizaciones


@app.route('/api/v1.0/organizacion/', methods=['GET'])
def muestraOrganizaciones():
    organizaciones = []

    for organizacion in Organizacion.query.all():
        organizaciones.append({
            "id_organizacion": organizacion.id_organizacion,
            "nombre": organizacion.nombre,
        })

    return json.dumps(organizaciones, indent=1, ensure_ascii=False).encode('utf8')


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/', methods=['GET'])
def muestraOrganizacion(organizacion_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        return jsonify({"id_organizacion": organizacion.id_organizacion, "nombre": organizacion.nombre})

    else:
        abort(404)


@app.route('/api/v1.0/organizacion/', methods=['POST'])
def insertaOrganizacion():
    value = request.json
    nombre = value["nombre"]

    orgIn = Organizacion(nombre)
    orgIn.post_organizacion()

    org = Organizacion().get_ult_organizacion()
    return jsonify({"id": org.id_organizacion, "nombre": org.nombre})


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/', methods=['PUT'])
def modificaOrganizacion(organizacion_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        value = request.json
        nombre = value["nombre"]

        organizacion.put_organizacion(nombre)

        return jsonify({"id_organizacion": organizacion.id_organizacion, "nombre": organizacion.nombre})
    else:
        abort(404)


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/', methods=['DELETE'])
def eliminaOrganizacion(organizacion_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        organizacion.delete_organizacion()
        return jsonify({"id_organizacion": organizacion.id_organizacion, "nombre": organizacion.nombre})
    else:
        abort(404)


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/usuarios/', methods=['GET'])
def muestraUsuariosOrg(organizacion_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        usuarios = []

        for usuario in organizacion.usuarios:
            usuarios.append({
                "id_usuario": usuario.id_usuario,
                "nombre": usuario.nombre,
                "apellidos": usuario.apellidos,
                "id_organizacion": organizacion_id
            })

        return json.dumps(usuarios, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/usuarios/<int:usuario_id>/', methods=['GET'])
def muestraUsuarioOrg(organizacion_id, usuario_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        if(organizacion.existe_organizacion_usuario(usuario_id)):
            usuario = Usuario().get_usuario(usuario_id)
            return jsonify({"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos, "id_organizacion" : organizacion_id})
        else:
            abort(404)
    else:
        abort(404)


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/usuarios/', methods=['POST'])
def insertaUsuarioOrg(organizacion_id):
    value = request.json
    nombre = value["nombre"]
    apellidos = value["apellidos"]

    organizacion = Organizacion().get_organizacion(organizacion_id)

    usuarioIn = Usuario(nombre, apellidos)
    usuarioIn.post_usuario()

    usuario = Usuario().get_ult_usuario()
    organizacion.put_organizacion_usuario(usuario)

    return jsonify({"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos" : usuario.apellidos, "id_organizacion" : organizacion_id})


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/usuarios/<int:usuario_id>/', methods=['PUT'])
def anyadeUsuarioOrg(organizacion_id, usuario_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if(organizacion):
        usuario = Usuario().get_usuario(usuario_id)
        if(usuario):
            usuario = Usuario().get_usuario(usuario_id)
            organizacion.put_organizacion_usuario(usuario)
            return jsonify({"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos, "id_organizacion" : organizacion_id})
        else:
            abort(404)
    else:
        abort(404)

@app.route('/api/v1.0/organizacion/<int:organizacion_id>/usuarios/<int:usuario_id>/', methods=['DELETE'])
def eliminaUsuarioOrg(organizacion_id, usuario_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)
    if(organizacion):
        if(organizacion.existe_organizacion_usuario(usuario_id)):
            usuario = Usuario().get_usuario(usuario_id)
            organizacion.delete_organizacion_usuario(usuario)

            return jsonify({"id_usuario": usuario.id_usuario, "nombre": usuario.nombre, "apellidos": usuario.apellidos, "id_organizacion" : organizacion_id})
        else:
            abort(404)
    else:
        abort(404)

@app.route('/api/v1.0/usuarios/<int:usuario_id>/organizacion/', methods=['GET'])
def muestraOrganizacionesUsu(usuario_id):
    usuario = Usuario().get_usuario(usuario_id)
    if(usuario):
        organizaciones = Organizacion().get_usuario_organizaciones(usuario_id)
        estructura = []

        for organizacion in organizaciones:
            estructura.append({
                "id_organizacion": organizacion.id_organizacion,
                "nombre": organizacion.nombre,
            })

        return json.dumps(estructura, indent=1, ensure_ascii=False).encode('utf8')

    else:
        abort(404)

@app.route('/api/v1.0/usuarios/<int:usuario_id>/organizacion/', methods=['GET'])
def muestraOrganizacionesUsu(usuario_id):
    usuario = Usuario().get_usuario(usuario_id)
    if(usuario):
        organizaciones = Organizacion().get_usuario_organizaciones(usuario_id)
        estructura = []

        for organizacion in organizaciones:
            estructura.append({
                "id_organizacion": organizacion.id_organizacion,
                "nombre": organizacion.nombre,
            })

        return json.dumps(estructura, indent=1, ensure_ascii=False).encode('utf8')

    else:
        abort(404)

@app.route('/api/v1.0/usuarios/<int:usuario_id>/organizacion/<int:organizacion_id>/', methods=['GET'])
def muestraOrganizacionUsu(usuario_id, organizacion_id):
    usuario = Usuario().get_usuario(usuario_id)
    if(usuario):
        organizaciones = Organizacion().get_usuario_organizaciones(usuario_id)

        for organizacion in organizaciones:
            if (organizacion.id_organizacion == organizacion_id):

                return "A"
    else:
        abort(404)
