
from db import db
from db import app
import numpy as np
from flask import jsonify, request
import json
from werkzeug.exceptions import abort, Response

class Pregunta(db.Model):
    id_pregunta = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.String(500))
    tipo_pregunta = db.Column(db.String(255))
    id_grupo = db.Column(db.Integer, db.ForeignKey('grupo.id_grupo'))
    id_area = db.Column(db.Integer, db.ForeignKey('area.id_area'))
    area = db.relationship('Area', backref='area')

    #area_pregunta = db.Column(db.Integer)
    #opciones = db.Column(db.Integer)

    def __init__(self, referencia='', tipo_pregunta='', id_grupo=0):
        self.ref = referencia
        self.tipo_pregunta = tipo_pregunta
        self.id_grupo = id_grupo

    def get_pregunta(self, id):
        pregunta = Pregunta.query.filter_by(id_pregunta=id).first()
        return pregunta

    def get_ult_pregunta(self):
        preguntas = Pregunta.query.all()

        numPreguntas = len(preguntas)
        pregunta = preguntas[numPreguntas - 1]

        return pregunta

    def post_pregunta(self):
        db.session.add(self)
        db.session.commit()

    def post_pregunta_area(self, area):
        self.area = area
        db.session.commit()

    #Edita la ref de preguntas
    def put_pregunta(self, ref, tipo_pregunta, id_grupo):
        self.ref = ref
        self.tipo_pregunta = tipo_pregunta
        self.id_grupo = id_grupo
        
        db.session.commit()

    def delete_pregunta(self):
        db.session.delete(self)
        db.session.commit()

    def existe_pregunta_id_ecoe(self, id_area):
        from Grupo import Grupo
        from Estacion import Estacion

        from Area import Area

        area = Area().get_area(id_area)

        if(area):
            id_ecoe_new = area.id_ecoe

            grupo = Grupo().get_grupo(self.id_grupo)
            estacion = Estacion().get_estacion(grupo.id_estacion)
            id_ecoe_old = estacion.id_ecoe

            if(id_ecoe_new==id_ecoe_old):
                return True
            else:
                return False


        else:
            return False

    def put_pregunta_area(self, id_area):
        self.id_area = id_area
        db.session.commit()

    def delete_pregunta_area(self):
        self.id_area = None
        db.session.commit()


# Relacion Pregunta-Area
@app.route('/api/v1.0/pregunta/<int:pregunta_id>/area/', methods=['GET'])
def obtenAreaPregunta(pregunta_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)

    if (pregunta):
        area = pregunta.area
        if(area):
            return jsonify({"id_area": area.id_area, "nombre": area.nombre})

        else:
            abort(404)
    else:
        abort(404)


@app.route('/api/v1.0/pregunta/<int:pregunta_id>/area/', methods=['PUT'])
def insertaAreaPregunta(pregunta_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)

    if (pregunta):
        value = request.json

        if not request.json or not "id_area" in request.json:
            abort(400)

        id_area = value["id_area"]

        if(pregunta.existe_pregunta_id_ecoe(id_area)):
            pregunta.put_pregunta_area(id_area)
            area = pregunta.area

            return jsonify({"id_area": area.id_area, "nombre": area.nombre})

        else:
            abort(404)

    else:
        abort(404)

@app.route('/api/v1.0/pregunta/<int:pregunta_id>/area/', methods=['DELETE'])
def eliminaAreaPregunta(pregunta_id):
    pregunta = Pregunta().get_pregunta(pregunta_id)

    if(pregunta):
        area = pregunta.area
        pregunta.delete_pregunta_area()

        return jsonify({"id_area": area.id_area, "nombre": area.nombre})
    else:
        abort(404)

