from app import db


class Shift(db.Model):
    __tablename__ = 'shift'

    id = db.Column(db.Integer, primary_key=True)
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'))
    shift_code = db.Column(db.String(20), nullable=False)
    time_start = db.Column(db.DateTime(), nullable=False)

    planners = db.relationship('Planner', backref='shift')

    __table_args__ = (
        db.UniqueConstraint(shift_code, id_ecoe, name='shift_ecoe_uk'),
    )