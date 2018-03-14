from  ws import db

class Chronometer(db.Model):
    __tablename__ = "chro"

    id_chronometer = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    total_time = db.Column(db.Integer)

