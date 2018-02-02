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

    def post_organizacion(self):
        organizacion = Organizacion(nombre=self.nombre)
        db.session.add(organizacion)

        db.session.commit()
        return organizacion

    #Editamos el nombre de la Organiación.
    def put_organizacion(self, nombre):
        organizacion = Organizacion.query.filter_by(id_organizacion=self.id_organizacion).first()
        organizacion.nombre = nombre
        db.session.commit()

        return organizacion

    def delete_organizacion(self):
        organizacion = Organizacion.query.filter_by(id_organizacion=self.id_organizacion).first()

        db.session.delete(organizacion)
        db.session.commit()

        return "OK"