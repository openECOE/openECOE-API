from db import db
from db import app
import numpy as np
from flask import jsonify, request
import json
from werkzeug.exceptions import abort, Response

from ECOE import ECOE

class Area(db.Model):
    id_area = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ECOE.id'))

    def __init__(self, nombre='', id_ecoe=0):
        self.nombre = nombre
        self.id_ecoe = id_ecoe

    def __repr__(self):
        return '<Area %r>' %self.nombre

    def post_area(self):

        db.session.add(self)
        db.session.commit()

    def get_area(self, id):
        area = Area.query.filter_by(id_area=id).first()
        return area

    def get_ult_area(self):
        areas = Area.query.all()

        numAreas = len(areas)
        area = areas[numAreas-1]

        return area

    def put_area(self, nombre, id_ecoe):
        self.nombre = nombre
        self.id_ecoe = id_ecoe
        db.session.commit()


    def delete_area(self):
        db.session.delete(self)
        db.session.commit()

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