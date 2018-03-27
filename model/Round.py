from model import db
from model.Shift import Shift

from sqlalchemy.orm import backref

class Round(db.Model):
    __tablename__="round"

    id_round = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    id_shift = db.Column(db.Integer, db.ForeignKey(Shift.id_shift), nullable=False)
    shift = db.relationship(Shift, backref=backref('rounds', lazy='dynamic'))
