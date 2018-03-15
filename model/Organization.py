from ws import db
from model import User, Orguser

class Organization(db.Model):
    __tablename__ = "org"
    id_organization = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    # orguser = db.relationship("Orguser")
