from db import db
from db import app
import numpy as np
from flask import jsonify, request
import json
from werkzeug.exceptions import abort, Response

from Area import Area
from Alumno import Alumno
from Estacion import Estacion
from Dia import Dia

class ECOE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    areas = db.relationship('Area', backref='areas', lazy='dynamic')
    alumnos = db.relationship('Alumno', backref='alumnos', lazy='dynamic')
    estaciones = db.relationship('Estacion', backref='estaciones', lazy='dynamic')
    dias = db.relationship('Dia', backref='dias', lazy='dynamic')
    #cronometros = db.relationship('Cronometro', backref='cronometros', lazy='dynamic')
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



#Relacion ECOE-Area
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/areas/', methods=['GET'])
def obtenAreas(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        areas = []
        for area in ecoe.areas:
            areas.append({
                "id_area" : area.id_area,
                "nombre" : area.nombre,
        })

        return json.dumps(areas, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/areas/<int:area_id>/', methods=['GET'])
def obtenArea(ecoe_id, area_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        if(ecoe.existe_ecoe_area(area_id)):
            area = Area().get_area(area_id)
            return jsonify({"id_area": area.id_area, "nombre": area.nombre})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/areas/', methods=['POST'])
def insertaArea(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        value = request.json

        if not request.json or not "nombre" in request.json:
            abort(400)

        nombre = value["nombre"]

        areaIn = Area(nombre=nombre, id_ecoe=ecoe_id)
        areaIn.post_area()

        area = Area().get_ult_area()

        return jsonify({"id_area" : area.id_area, "nombre" : area.nombre})
    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/areas/<int:area_id>/', methods=['PUT'])
def modificaArea(ecoe_id, area_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        if (ecoe.existe_ecoe_area(area_id)):
            value = request.json

            if ((not request.json) or (not "nombre" in request.json) or (not "id_ecoe" in request.json)):
                abort(400)

            nombre = value["nombre"]
            id_ecoe = value["id_ecoe"]

            area = Area().get_area(area_id)
            area.put_area(nombre, id_ecoe)

            return jsonify({"id_area": area.id_area, "nombre": area.nombre})
        else:
            abort(404)

    else:
        abort(404)



@app.route('/api/v1.0/ECOE/<int:ecoe_id>/areas/<int:area_id>/', methods=['DELETE'])
def eliminaArea(ecoe_id, area_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        if (ecoe.existe_ecoe_area(area_id)):
            area = Area().get_area(area_id)
            area.delete_area()

            return jsonify({"id_area": area.id_area, "nombre": area.nombre})
        else:
            abort(404)

    else:
        abort(404)


#Relacion ECOE-Alumno
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/alumno/', methods=['GET'])
def obtenAlumnos(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        alumnos = []
        for alumno in ecoe.alumnos:
            alumnos.append({
                "id_area" : alumno.id_alumno,
                "nombre" : alumno.nombre,
                "DNI" : alumno.dni
        })

        return json.dumps(alumnos, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/alumno/<int:alumno_id>/', methods=['GET'])
def obtenAlumno(ecoe_id, alumno_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        if(ecoe.existe_ecoe_alumno(alumno_id)):
            alumno = Alumno().get_alumno(alumno_id)
            return jsonify({"id_alumno": alumno.id_alumno, "nombre": alumno.nombre, "dni" : alumno.dni})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/alumno/', methods=['POST'])
def insertaAlumno(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        value = request.json

        if ((not request.json) or (not "nombre" in request.json) or (not "dni" in request.json)):
            abort(400)

        nombre = value["nombre"]
        dni = value["dni"]

        alumnoIn = Alumno(nombre, dni, ecoe_id)
        alumnoIn.post_alumno()

        alumno = Alumno().get_ult_alumno()

        return jsonify({"id_alumno": alumno.id_alumno, "nombre": alumno.nombre, "dni": alumno.dni})
    else:
        abort(404)



@app.route('/api/v1.0/ECOE/<int:ecoe_id>/alumno/<int:alumno_id>/', methods=['PUT'])
def modificaAlumno(ecoe_id, alumno_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        if (ecoe.existe_ecoe_alumno(alumno_id)):
            value = request.json

            if ((not request.json) or (not "nombre" in request.json)  or (not "dni" in request.json) or (not "id_ecoe" in request.json)):
                abort(400)

            nombre = value["nombre"]
            dni = value["dni"]
            id_ecoe = value["id_ecoe"]

            alumno = Alumno().get_alumno(alumno_id)
            alumno.put_alumno(nombre, dni, id_ecoe)

            return jsonify({"id_alumno": alumno.id_alumno, "nombre": alumno.nombre, "dni": alumno.dni})
        else:
            abort(404)

    else:
        abort(404)




@app.route('/api/v1.0/ECOE/<int:ecoe_id>/alumno/<int:alumno_id>/', methods=['DELETE'])
def eliminaAlumno(ecoe_id, alumno_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        if (ecoe.existe_ecoe_alumno(alumno_id)):
            alumno = Alumno().get_alumno(alumno_id)
            alumno.delete_alumno()

            return jsonify({"id_alumno": alumno.id_alumno, "nombre": alumno.nombre, "dni": alumno.dni})
        else:
            abort(404)

    else:
        abort(404)

#Relacion ECOE-Estacion
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estacion/', methods=['GET'])
def obtenEstaciones(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        estaciones = []
        for estacion in ecoe.estaciones:
            estaciones.append({
                "id_estacion" : estacion.id_estacion,
                "nombre" : estacion.nombre
        })

        return json.dumps(estaciones, indent=1, ensure_ascii=False).encode('utf8')
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estacion/<int:estacion_id>/', methods=['GET'])
def obtenEstacion(ecoe_id, estacion_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        if(ecoe.existe_ecoe_estacion(estacion_id)):
            estacion = Estacion().get_estacion(estacion_id)
            return jsonify({"id_estacion": estacion.id_estacion, "nombre": estacion.nombre})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estacion/', methods=['POST'])
def insertaEstacion(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if(ecoe):
        value = request.json

        if ((not request.json) or (not "nombre" in request.json)):
            abort(400)

        nombre = value["nombre"]

        estacionIn = Estacion(nombre, ecoe_id)
        estacionIn.post_estacion()

        estacion = Estacion().get_ult_estacion()

        return jsonify({"id_estacion" : estacion.id_estacion, "nombre" : estacion.nombre})
    else:
        abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estacion/<int:estacion_id>/', methods=['PUT'])
def modificaEstacion(ecoe_id, estacion_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        if (ecoe.existe_ecoe_estacion(estacion_id)):
            value = request.json

            if ((not request.json) or (not "nombre" in request.json) or (not "id_ecoe" in request.json)):
                abort(400)

            nombre = value["nombre"]
            id_ecoe = value["id_ecoe"]

            estacion = Estacion().get_estacion(estacion_id)
            estacion.put_estacion(nombre, id_ecoe)

            return jsonify({"id_estacion": estacion.id_estacion, "nombre": estacion.nombre, "id_ecoe": estacion.id_ecoe})
        else:
            abort(404)

    else:
        abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/estacion/<int:estacion_id>/', methods=['DELETE'])
def eliminaEstacion(ecoe_id, estacion_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    if (ecoe):
        if (ecoe.existe_ecoe_estacion(estacion_id)):
            estacion = Estacion().get_estacion(estacion_id)
            estacion.delete_estacion()

            return jsonify({"id_estacion": estacion.id_estacion, "nombre": estacion.nombre, "id_ecoe": estacion.id_ecoe})
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


