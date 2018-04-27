from app import db


class Chronometer(db.Model):
    __tablename__ = 'chronometer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    total_time = db.Column(db.Integer, nullable=False)

    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'), nullable=False)

    alarms = db.relationship('Alarm', backref='chrono')
    stations = db.relationship('Station', backref='chrono')
