from db import db
import numpy as np

class Organizacion(db.Model):
    id_organizacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    #usuarios = db.relationship('Usuario', backref='usuarios', lazy='dynamic' )
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



    #TODO falta los metodos relacionados con el Array de Usuarios
