from db import db
from db import app
import numpy as np
from Usuario import Usuario

from werkzeug.exceptions import abort, Response


from flask import Flask, jsonify, request

class Organizacion(db.Model):
    id_organizacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    usuarios = db.relationship('Usuario', backref='usuarios', lazy='dynamic' )
    #ecoes = db.relationship('ECOE', backref='ecoes', lazy='dynamic')

    def __init__(self, nombre=''):
        self.nombre = nombre
       # self.usuarios = usuarios
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


@app.route('/api/v1.0/organizacion/', methods=['GET'])
def muestraOrganizaciones():
    return "Hola"


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/', methods=['GET'])
def muestraOrganizacion(organizacion_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        return jsonify({"id_organizacion": organizacion.id_organizacion, "nombre": organizacion.nombre})

    else:
        abort(404)
        # abort(Response("Error"))


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


