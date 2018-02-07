from db import db
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

    def put_area(self, nombre):
        self.nombre = nombre
        db.session.commit()


    def delete_area(self):
        db.session.delete(self)
        db.session.commit()

# Rutas de Area, (faltan por insertar los id de las ECOE)
@app.route('/api/v1.0/ECOE/<int:ecoe_id>/areas/', methods=['GET'])
def obtenAreas(ecoe_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    arrAreasID = []
    arrAreasNombre = []

    for i in ecoe.areas.all():
       arrAreasID.append(i.id_area)
       arrAreasNombre.append(i.nombre)

    return jsonify({"id" : ecoe.id, "nombre" : ecoe.nombre, "id_areas" : arrAreasID, "nombres_areas" : arrAreasNombre})


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/areas/<int:area_id>/', methods=['GET'])
def obtenArea(ecoe_id, area_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    for i in ecoe.areas.all():
        if area_id == i.id_area:
            area = Area().get_area(area_id)
            return jsonify({"id_area": area.id_area, "nombre": area.nombre})

    abort(404)

@app.route('/api/v1.0/ECOE/<int:ecoe_id>/areas/', methods=['POST'])
def insertaArea(ecoe_id):

    value = request.json
    nombre = value["nombre"]

    areaIn = Area(nombre=nombre, id_ecoe=ecoe_id)
    areaIn.post_area()

    area = Area().get_ult_area()

    return jsonify({"id_area" : area.id_area, "nombre" : area.nombre, "id_ecoe" : area.id_ecoe})


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/areas/<int:area_id>/', methods=['PUT'])
def modificaArea(ecoe_id, area_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    value = request.json
    nombre = value["nombre"]

    for i in ecoe.areas.all():
        if area_id == i.id_area:
            area = Area().get_area(area_id)
            area.put_area(nombre)
            return jsonify({"id_area": area.id_area, "nombre": area.nombre})

    abort(404)


@app.route('/api/v1.0/ECOE/<int:ecoe_id>/areas/<int:area_id>/', methods=['DELETE'])
def eliminaArea(ecoe_id, area_id):
    ecoe = ECOE().get_ECOE(ecoe_id)

    for i in ecoe.areas.all():
        if area_id == i.id_area:
            area = Area().get_area(area_id)
            area.delete_area()
            return jsonify({"id_area": area.id_area, "nombre": area.nombre, "id_ecoe": area.id_ecoe})

    abort(404)
