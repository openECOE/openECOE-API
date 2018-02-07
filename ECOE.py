import numpy as np


from Area import Area
from Alumno import Alumno
from Estacion import Estacion
from Dia import Dia
from Cronometro import Cronometro

from db import db
import numpy as np

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

    def get_ECOEs_id(self):
        ids = ECOE.query.with_entities(ECOE.id).all()
        return list(np.squeeze(ids))

    def get_ECOEs_nombres(self):
        nombres = ECOE.query.with_entities(ECOE.nombre).all()
        return list(np.squeeze(nombres))

    def get_ECOE(self, id):
        ecoe = ECOE.query.filter_by(id=id).first()
        return ecoe;

    def get_ult_ecoe(self):
        ecoes = ECOE.query.all()

        numEcoes = len(ecoes)
        ecoe = ecoes[numEcoes-1]

        return ecoe


    def post_ecoe(self):
        ecoe = ECOE(nombre=self.nombre)

        db.session.add(ecoe)
        db.session.commit()

    def put_ecoe(self, nombre):
        self.nombre = nombre
        db.session.commit()

    def delete_ecoe(self):
        db.session.delete(self)
        db.session.commit()


#Rutas de ECOE
@app.route('/api/v1.0/ECOE/', methods=['GET'])
def muestraECOEs():
    ids = ECOE().get_ECOEs_id()
    nombres = ECOE().get_ECOEs_nombres()

    return jsonify({"ids" : ids, "nombres" : nombres})


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/', methods=['GET'])
def muestraECOE(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)
    if(ecoe):
        return jsonify({"id": ecoe.id, "nombre": ecoe.nombre})
    else:
        abort(404)
        #abort(Response("Error"))

@app.route('/api/v1.0/ECOE/', methods=['POST'])
def insertaECOE():
    value = request.json
    nombre = value["nombre"]

    ecoeIn = ECOE(nombre)
    ecoeIn.post_ecoe()

    ecoe = ECOE().get_ult_ecoe()
    return jsonify({"id" : ecoe.id, "nombre" : ecoe.nombre})


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/', methods=['PUT'])
def actualizaECOE(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        value = request.json
        nombre = value["nombre"]

        ecoe.put_ecoe(nombre)
        return jsonify({"id": ecoe.id, "nombre": ecoe.nombre})
    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/', methods=['DELETE'])
def eliminaECOE(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        ecoe.delete_ecoe()
        return jsonify({"id": ecoe.id, "nombre": ecoe.nombre})
    else:
        abort(404)
