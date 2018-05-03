from app import db


class Wheel(db.Model):
    __tablename__ = 'wheel'

    id = db.Column(db.Integer, primary_key=True)
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'))
    wheel_code = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    planners = db.relationship('Planner', backref='wheel')

    __table_args__ = (
        db.UniqueConstraint(wheel_code, id_ecoe, name='wheel_ecoe_uk'),
    )

