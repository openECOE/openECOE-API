from Area import Area
from Alumno import Alumno
from Estacion import Estacion
from Dia import Dia
from Cronometro import Cronometro

from db import db


class ECOE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    areas = db.relationship('Area', backref='areas', lazy='dynamic')
    #alumnos = db.relationship('Alumno', backref='alumnos', lazy='dynamic')
    #estaciones = db.relationship('Estacion', backref='estaciones', lazy='dynamic')
    #dias = db.relationship('Dia', backref='dias', lazy='dynamic')
    #cronometros = db.relationship('Cronometro', backref='cronometros', lazy='dynamic')

    def __init__(self, nombre=''):
        self.nombre = nombre


    def __repr__(self):
        return '<ECOE %r>' %self.nombre

    def get_ECOE(self, id):
        ecoe = ECOE.query.filter_by(id=id).first()
        return ecoe

    def get_ult_ecoe(self):
        ecoes = ECOE.query.all()

        numEcoes = len(ecoes)
        ecoe = ecoes[numEcoes-1]

        return ecoe


    def post_ecoe(self):
        ecoe = ECOE(nombre=self.nombre)

        db.session.add(ecoe)
        db.session.commit()

