from app import db
import enum

class TurnType(enum.Enum):
    MORNING = "M"
    AFTERNOON = "T"


class Turn(db.Model):
    __tablename__ = 'turn'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Enum(TurnType), nullable=False)
    id_day = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=False)
    time_start = db.Column(db.String(5))  # HH:MM

    wheels = db.relationship('Wheel', backref='turn')

    __table_args__ = (
        db.UniqueConstraint('code', 'id_day', name='turn_day_uc'),
    )

