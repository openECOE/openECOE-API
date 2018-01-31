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

    def get_area(self, id):
        area = Area.query.filter_by(id_area=id).first()
        return area

