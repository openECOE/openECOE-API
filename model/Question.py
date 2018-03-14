from ws import db
from sqlalchemy.orm import backref
from model import Area, Group

class Question(db.Model):
    __tablename__ = "ques"

    id_question = db.Column(db.Integer, primary_key=True)
    id_group = db.Column(db.Integer, db.ForeignKey("group.id_group"), nullable=False)
    group = db.relationship("Group", backref=backref('questionsgroup', lazy='dynamic'))
    id_area = db.Column(db.Integer, db.ForeignKey("area.id_area"), nullable=False)
    area = db.relationship("Area", backref='questionsarea') #Esta relación no debe de ser inversa
    ref = db.Column(db.String(255))
    option_type = db.Column(db.String(500))
