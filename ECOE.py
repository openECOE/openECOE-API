from db import db
from db import app
import numpy as np
from flask import jsonify, request
import json
from werkzeug.exceptions import abort, Response

from Organizacion import Organizacion

class ECOE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    areas = db.relationship('Area', backref='areas', lazy='dynamic')
    alumnos = db.relationship('Alumno', backref='alumnos', lazy='dynamic')
    estaciones = db.relationship('Estacion', backref='estaciones', lazy='dynamic')
    dias = db.relationship('Dia', backref='dias', lazy='dynamic')
    cronometros = db.relationship('Cronometro', backref='cronometros', lazy='dynamic')
    id_organizacion = db.Column(db.Integer, db.ForeignKey('organizacion.id_organizacion'))

    def __init__(self, nombre='', id_organizacion=0):
        self.nombre = nombre
        self.id_organizacion = id_organizacion

    def __repr__(self):
        return '<ECOE %r>' %self.nombre

    #def get_ECOEs_id(self):
     #   ids = ECOE.query.with_entities(ECOE.id).all()
     #   return list(np.squeeze(ids))

    def get_ECOE(self, id):
        ecoe = ECOE.query.filter_by(id=id).first()
        return ecoe;

    def get_ult_ecoe(self):
        ecoes = ECOE.query.all()

        numEcoes = len(ecoes)
        ecoe = ecoes[numEcoes-1]

        return ecoe


    def post_ecoe(self):
        db.session.add(self)
        db.session.commit()

    def put_ecoe(self, nombre, id_organizacion):
        self.nombre = nombre
        self.id_organizacion = id_organizacion
        db.session.commit()


    def delete_ecoe(self):
        db.session.delete(self)
        db.session.commit()

    def existe_ecoe_area(self, id_area):
        for area in self.areas:
            if(area.id_area==id_area):
                return True
        return False

    def existe_ecoe_alumno(self, id_alumno):
        for alumno in self.alumnos:
            if(alumno.id_alumno==id_alumno):
                return True
        return False

    def existe_ecoe_estacion(self, id_estacion):
        for estacion in self.estaciones:
            if(estacion.id_estacion==id_estacion):
                return True
        return False


#Rutas de Organizacion-ECOE
@app.route('/api/v1.0/organizacion/<int:organizacion_id>/ECOE/', methods=['GET'])
def muestraEcoesOrganizacion(organizacion_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    ecoes=[]

    if(organizacion):
        for ecoe in organizacion.ecoes:
            ecoes.append({
                "id" : ecoe.id,
                "nombre" : ecoe.nombre,
            })

        return json.dumps(ecoes, indent=1, ensure_ascii=False).encode('utf8')

    else:
        abort(404)


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/ECOE/<int:ecoe_id>/', methods=['GET'])
def muestraEcoeOrganizacion(organizacion_id, ecoe_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if(organizacion):
        if(organizacion.existe_organizacion_ecoe(ecoe_id)):
            ecoe = ECOE().get_ECOE(ecoe_id)
            return jsonify({"id": ecoe.id, "nombre": ecoe.nombre})
        else:
            abort(404)
    else:
        abort(404)


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/ECOE/', methods=['POST'])
def creaEcoeOrganizacion(organizacion_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)
    if(organizacion):
        value = request.json

        if not request.json or not "nombre" in request.json:
            abort(400)

        nombre = value["nombre"]

        ecoe = ECOE(nombre, organizacion_id)
        ecoe.post_ecoe()

        return jsonify({"id": ecoe.id, "nombre": ecoe.nombre})
    else:
        abort(404)


@app.route('/api/v1.0/organizacion/<int:organizacion_id>/ECOE/<int:ecoe_id>/', methods=['PUT'])
def modificaEcoeOrganizacion(organizacion_id, ecoe_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if(organizacion):
        if(organizacion.existe_organizacion_ecoe(ecoe_id)):
            value = request.json

            if ((not request.json) or (not "nombre" in request.json) or (not "id_organizacion" in request.json)):
                abort(400)

            nombre = value["nombre"]
            id_organizacion = value["id_organizacion"]

            ecoe = ECOE().get_ECOE(ecoe_id)
            ecoe.put_ecoe(nombre, id_organizacion)

            return jsonify({"id": ecoe.id, "nombre": ecoe.nombre})
        else:
            abort(404)
    else:
        abort(404)




@app.route('/api/v1.0/organizacion/<int:organizacion_id>/ECOE/<int:ecoe_id>/', methods=['DELETE'])
def eliminaEcoeOrganizacion(organizacion_id, ecoe_id):
    organizacion = Organizacion().get_organizacion(organizacion_id)

    if (organizacion):
        if (organizacion.existe_organizacion_ecoe(ecoe_id)):

            ecoe = ECOE().get_ECOE(ecoe_id)
            ecoe.delete_ecoe()

            return jsonify({"id": ecoe.id, "nombre": ecoe.nombre})
        else:
            abort(404)
    else:
        abort(404)





#RUTAS DE DIA (En desarrollo)

#No esta la ruta para visualizar todos los dias

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>', methods=['GET'])
def muestraDia(dia_id):
    ecoe = ECOE().get_ECOE()

    if(ecoe):


        return "AAAAAAAA"

    else:
        abort(404)



@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias', methods=['POST'])
def insertaDia(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        value = request.json
        fecha = value["fecha"]

        diaIn = Dia(fecha=fecha, id_ecoe=ecoe_id)
        diaIn.post_dia()

        dia = Dia().get_ult_dia()

        return jsonify({"id_dia": dia.id_dia, "fecha": dia.fecha})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>', methods=['PUT'])
def modificaDia(dia_id):
    dia = Dia().get_dia(dia_id)

    if(dia):
        value = request.json
        fecha = value["fecha"]

        dia.put_dia(fecha)

        return jsonify({"id_dia": dia.id_dia, "fecha": dia.fecha})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/dias/<int:dia_id>', methods=['DELETE'])
def eliminaDia(dia_id):
    dia = Dia().get_dia(dia_id)

    if(dia):
        dia.delete_dia()
        return jsonify({"id_dia": dia.id_dia, "fecha": dia.fecha})
    else:
        abort(404)


