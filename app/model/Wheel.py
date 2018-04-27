from app import db

class Wheel(db.Model):
    __tablename__ = 'wheel'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), nullable=False)
    id_turn = db.Column(db.Integer, db.ForeignKey('turn.id'), nullable=False)
    description = db.Column(db.String(255))

    students = db.relationship('Student', backref='wheel')

    __table_args__ = (
        db.UniqueConstraint('code', 'id_turn', name='wheel_turn_uc'),
    )

