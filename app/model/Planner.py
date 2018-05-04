from app import db


class Planner(db.Model):
    __tablename__ = 'planner'

    id = db.Column(db.Integer, primary_key=True)
    id_shift = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=False)
    id_round = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False)

    students = db.relationship('Student', backref='planner')

    __table_args__ = (
        db.UniqueConstraint(id_shift, id_round, name='shift_round_uk'),
    )