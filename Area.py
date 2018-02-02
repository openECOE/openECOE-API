from db import db

class Area(db.Model):
    id_area = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))

    def __init__(self, nombre=''):
        self.nombre = nombre

    def __repr__(self):
        return '<Area %r>' %self.area

    def post_area(self):
        area = Area(nombre=self.nombre)
        db.session.add(area)

        db.session.commit()
        return area

    def get_area(self, id):
        area = Area.query.filter_by(id_area=id).first()
        return area


    def get_ult_area(self):
        areas = Area.query.all()

        numAreas = len(areas)
        area = areas[numAreas-1]

        return area

    def put_area(self, nombre):
        area = Area.query.filter_by(id_area=self.id_area).first()
        area.nombre = nombre
        db.session.commit()

        return area

    def delete_area(self):
        area = Area.query.filter_by(id_area=self.id_area).first()

        db.session.delete(area)
        db.session.commit()

        return "OK"