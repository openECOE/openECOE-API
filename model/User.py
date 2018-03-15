from model import db
from model import Permission

class User(db.Model):
    __tablename__ = "user"
    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    userperm = db.relationship("Userperm")


class Userperm(db.Model):
    __tablename__ = "userperm"
    id_user = db.Column(db.Integer, db.ForeignKey("user.id_user"), primary_key=True)
    id_permission = db.Column(db.Integer, db.ForeignKey("perm.id_permission"), primary_key=True)
    user = db.relationship("User")