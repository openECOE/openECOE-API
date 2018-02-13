from db import db
from db import app
import numpy as np
from flask import jsonify, request
import json
from werkzeug.exceptions import abort, Response

class Cronometro(db.Model):
    id_cronometro = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    tiempo_total = db.Column(db.Integer)
    id_estacion = db.Column(db.Integer, db.ForeignKey('estacion.id_estacion'))

    #alarmas = db.Column(db.Integer)

    def __init__(self, nombre='', tiempo_total=0, id_estacion=0):
        self.nombre = nombre
        self.tiempo_total = tiempo_total
        self.id_estacion = id_estacion


        #self.alarmas = alarmas

    def get_cronometro(self, id):
        cronometro = Cronometro.query.filter_by(id_cronometro=id).first()
        return cronometro

    def get_ult_cronometro(self):
        cronometros = Cronometro.query.all()

        numCronometros = len(cronometros)
        cronometro = cronometros[numCronometros - 1]

        return cronometro


    def post_cronometro(self):
        db.session.add(self)
        db.session.commit()

    def put_cronometro(self, nombre, tiempo_total, id_estacion):
        self.nombre = nombre
        self.tiempo_total = tiempo_total
        self.id_estacion = id_estacion
        db.session.commit()


    def delete_cronometro(self):
        db.session.delete(self)
        db.session.commit()

