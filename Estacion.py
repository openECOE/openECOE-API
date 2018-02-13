from db import db

class Estacion(db.Model):
    id_estacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ECOE.id'))


    def __init__(self, nombre='', id_ecoe=''):
        self.nombre = nombre
        self.id_ecoe = id_ecoe
        #self.grupos = grupos
        #self.cronometros = cronometros

    def get_estacion(self, id):
        estacion = Estacion.query.filter_by(id_estacion=id).first()
        return estacion

    def get_ult_estacion(self):
        estaciones = Estacion.query.all()

        numEstacion = len(estaciones)
        estacion = estaciones[numEstacion-1]

        return estacion

    def post_estacion(self):
        db.session.add(self)
        db.session.commit()

    def put_estacion(self, nombre, id_ecoe):
        self.nombre = nombre
        self.id_ecoe = id_ecoe
        db.session.commit()

    def delete_estacion(self):
        db.session.delete(self)
        db.session.commit()
