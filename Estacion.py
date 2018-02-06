from db import db

class Estacion(db.Model):
    id_estacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))

    # TODO hacer que grupos y cronometros sea relationship
    grupos = db.Column(db.Integer)
    cronometros = db.Column(db.Integer)

    def __init__(self, nombre, grupos=[], cronometros=[]):
        self.nombre = nombre
        self.grupos = grupos
        self.cronometros = cronometros

    def get_estacion(self, id):
        estacion = Estacion.query.filter_by(id_estacion=id).first()
        return estacion

    def post_estacion(self):
        db.session.add(self)
        db.session.commit()

    def put_estacion(self, nombre):
        self.nombre = nombre
        db.session. commit()

    def delete_estacion(self):
        db.session.delete(self)
        db.session.commit()

    #TODO faltan los métodos relacionados con Grupos y Cronometros