from ws import db

class Area(db.Model):
    __tablename__ = "area"

    id_area = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ECOE.id'))

    def __init__(self, nombre='', id_ecoe=0):
        self.name = nombre
        self.id_ecoe = id_ecoe

    def __repr__(self):
        return '<Area %r>' %self.name

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
        self.name = nombre
        self.id_ecoe = id_ecoe
        db.session.commit()


    def delete_area(self):
        db.session.delete(self)
        db.session.commit()

