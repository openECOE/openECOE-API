from ws import db
from model import Userperm, Permission

class User(db.Model):
    __tablename__ = "user"
    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    userperm = db.relationship("Userperm")


