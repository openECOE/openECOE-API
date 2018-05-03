from app import db


class Wheel(db.Model):
    __tablename__ = 'wheel'

    id = db.Column(db.Integer, primary_key=True)
    wheel_code = db.Column(db.String(100), nullable=False)
    id_shift = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=False)
    description = db.Column(db.String(255))

    students = db.relationship('Student', backref='wheel')

    __table_args__ = (
        db.UniqueConstraint(wheel_code, id_shift, name='wheel_shift_uk'),
    )

