from app import db


class ECOE(db.Model):
    __tablename__ = 'ecoe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    id_organization = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)

    areas = db.relationship('Area', backref='ecoe')
    stations = db.relationship('Station', backref='ecoe')
    schedules = db.relationship('Schedule', backref='ecoe')
    students = db.relationship('Student', backref='ecoe')
    rounds = db.relationship('Round', backref='ecoe')
    shifts = db.relationship('Shift', backref='ecoe')



