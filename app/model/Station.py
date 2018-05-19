from app import db
from sqlalchemy.event import listen

class Station(db.Model):
    __tablename__ = 'station'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'), nullable=False)
    order = db.Column(db.Integer)

    schedules = db.relationship('Schedule', backref='station')
    qblocks = db.relationship('QBlock', backref='station')

    __table_args__ = (
        db.UniqueConstraint(name, id_ecoe, name='station_ecoe_uk'),
    )