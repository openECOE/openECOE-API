from model import db
from sqlalchemy.orm import backref
from model.Group import Group
from model.Area import Area

class Question(db.Model):
    __tablename__ = "ques"

    id_question = db.Column(db.Integer, primary_key=True)
    id_group = db.Column(db.Integer, db.ForeignKey(Group.id_group), nullable=False)
    group = db.relationship(Group, backref=backref('questions', lazy='dynamic'))
    id_area = db.Column(db.Integer, db.ForeignKey(Area.id_area), nullable=False)
    area = db.relationship(Area, backref='area') #Esta relación no debe de ser inversa
    ref = db.Column(db.String(255))
    option_type = db.Column(db.String(500))
