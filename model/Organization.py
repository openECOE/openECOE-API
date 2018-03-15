from model import db

class Organization(db.Model):
    __tablename__ = "org"
    id_organization = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    # orguser = db.relationship("Orguser")

# class Orguser(db.Model):
#     __tablename__ = "orguser"
#     id_organization = db.Column(db.Integer, db.ForeignKey("org.id_organization"), primary_key=True)
#     id_user = db.Column(db.Integer, db.ForeignKey("user.id_user"), primary_key=True)
#     organization = db.relationship("Organization")