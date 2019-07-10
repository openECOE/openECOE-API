from app import db

class Station(db.Model):
    __tablename__ = 'station'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'), nullable=False)
    order = db.Column(db.Integer)
    id_parent_station = db.Column(db.Integer, db.ForeignKey('station.id'))

    schedules = db.relationship('Schedule', backref='station')
    qblocks = db.relationship('QBlock', backref='station')

    # adjacency list pattern
    children_stations = db.relationship('Station', backref=db.backref('parent_station', remote_side=[id]))

    __table_args__ = (
        db.UniqueConstraint(name, id_ecoe, name='station_ecoe_uk'),
        db.Index('ix_station_parent', id_parent_station)
)