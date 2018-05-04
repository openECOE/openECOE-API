from app import db


class Organization(db.Model):
    __tablename__ = 'organization'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    users = db.relationship('User', backref='organization')
    ecoes = db.relationship('ECOE', backref='organization')


