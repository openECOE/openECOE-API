from app import db


class Stage(db.Model):
    __tablename__ = 'stage'

    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer, nullable=False)  # in seconds
    order = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    schedules = db.relationship('Schedule', backref='stage')

