from model import db
from sqlalchemy.orm import backref



class Student(db.Model):
    __tablename__="stu"

    id_student = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    dni = db.Column(db.String(25))
