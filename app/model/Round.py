from app import db


class Round(db.Model):
    __tablename__ = 'round'

    id = db.Column(db.Integer, primary_key=True)
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'))
    round_code = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    planners = db.relationship('Planner', backref='round')

    __table_args__ = (
        db.UniqueConstraint(round_code, id_ecoe, name='round_ecoe_uk'),
    )

