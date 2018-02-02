from db import db

class Organizacion(db.Model):
    id_organizacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    usuarios = db.Column(db.String(255))
    ecoes = db.Column(db.Integer)

    def __init__(self, nombre='', usuarios=[], ecoes=[]):
        self.nombre = nombre
        self.usuarios = usuarios
        self.ecoes = ecoes


    def get_organizacion(self, id):
        organizacion = Organizacion.query.filter_by(id_organizacion=id).first()
        return organizacion
