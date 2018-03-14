from ws import db
from model import Organization, User

class Orguser(db.Model):
    __tablename__ = "orguser"
    id_organization = db.Column(db.Integer, db.ForeignKey("org.id_organization"), primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id_user"), primary_key=True)
    organization = db.relationship("Organization")