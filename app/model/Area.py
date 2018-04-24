from sqlalchemy.orm import backref
from app import db
from .ECOE import ECOE


class Area(db.Model):
    __tablename__ = 'area'

    id_area = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(257))
    id_ecoe = db.Column(db.Integer, db.ForeignKey(ECOE.id), nullable=False)
    ecoe = db.relationship(ECOE, backref=backref('areas', lazy='dynamic'))

    def get_area(self, id):
        area = Area.query.filter_by(id_area=id).first()
        return area