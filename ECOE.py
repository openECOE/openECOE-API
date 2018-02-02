from Area import Area
from Alumno import Alumno
from Estacion import Estacion
from Dia import Dia
from Cronometro import Cronometro

from db import db

class ECOE:
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))


    def __init__(self, nombre='', areas = [], alumnos=[], estaciones=[], dias=[], cronometros=[]):
        self.nombre = nombre
        self.areas = areas
        self.alumnos = alumnos
        self.estaciones = estaciones
        self.dias = dias
        self.cronometros = cronometros

    def __repr__(self):
        return '<Nombre %r>' %self.nombre