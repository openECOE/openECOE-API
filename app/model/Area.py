from app import db


class Area(db.Model):
    __tablename__ = 'area'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'), nullable=False)

    questions = db.relationship('Question', backref='area')



