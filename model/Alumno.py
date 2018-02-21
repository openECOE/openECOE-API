from db import db
from db import app
import numpy as np
from flask import jsonify, request
import json
from werkzeug.exceptions import abort, Response

from ECOE import ECOE

class Alumno(db.Model):
    id_alumno = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    dni = db.Column(db.String(25))
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ECOE.id'))

    def __init__(self, nombre='', dni='', id_ecoe=0):
        self.nombre = nombre
        self.dni = dni
        self.id_ecoe = id_ecoe

    def get_alumno(self, id):
        alumno = Alumno.query.filter_by(id_alumno=id).first()
        return alumno

    def post_alumno(self):
        db.session.add(self)
        db.session.commit()

    def put_alumno(self, nombre, dni, id_ecoe):
        self.dni = dni
        self.nombre = nombre
        self.id_ecoe = id_ecoe
        db.session.commit()


    def delete_alumno(self):
        db.session.delete(self)
        db.session.commit()

    def get_ult_alumno(self):
        alumnos = Alumno.query.all()

        numAlumnos = len(alumnos)
        alumno = alumnos[numAlumnos-1]

        return alumno

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
