from app import db


class Schedule(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.Integer, primary_key=True)

    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'))
    id_stage = db.Column(db.Integer, db.ForeignKey('stage.id'), nullable=False)
    id_station = db.Column(db.Integer, db.ForeignKey('station.id'))

    events = db.relationship('Event', backref='schedule')

    __table_args__ = (
        db.UniqueConstraint('id_ecoe', 'id_stage', name='ecoe_stage_uc'),
        db.UniqueConstraint('id_station', 'id_stage', name='station_stage_uc'),
    )
