from app import db

class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    sound = db.Column(db.String(550), nullable=False)
    id_schedule = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)

