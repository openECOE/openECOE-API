from ws import db
from model import Cronometro

estCrono = db.Table('estCrono', db.Column('id_estacion', db.Integer, db.ForeignKey('estacion.id_estacion'), primary_key=True), db.Column('id_cronometro', db.Integer, db.ForeignKey('cronometro.id_cronometro'), primary_key=True))

class Estacion(db.Model):
    id_estacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ECOE.id'))
    grupos = db.relationship('Grupo', backref='grupos', lazy='dynamic')
    cronometros = db.relationship('Cronometro', secondary=estCrono, lazy='subquery', backref=db.backref('estCro', lazy='dynamic'))

    def __init__(self, nombre='', id_ecoe='', grupos=[], cronometros=[]):
        self.nombre = nombre
        self.id_ecoe = id_ecoe
        self.grupos = grupos
        self.cronometros = cronometros

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

    def existe_estacion_grupos(self, id_grupo):
        for grupo in self.grupos:
            if(grupo.id_grupo==id_grupo):
                return True
        return False

    def existe_estacion_cronometro(self, id_cronometro):
        for cronometro in self.cronometros:
            if(cronometro.id_cronometro==id_cronometro):
                return True
        return False

    def put_estacion_cronometro(self, cronometro):
        self.cronometros.append(cronometro)
        db.session.commit()

    def delete_estacion_cronometro(self, cronometro):
        self.cronometros.remove(cronometro)
        db.session.commit()

