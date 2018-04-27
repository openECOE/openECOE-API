from app import db


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surnames = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(10), nullable=False, unique=True)

    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'), nullable=False)
    id_wheel = db.Column(db.Integer, db.ForeignKey('wheel.id'))

    answers = db.relationship('Answer', backref='student')
