from sqlalchemy.orm import backref

from ws import db
from model import User, Permission

class Userperm(db.Model):
    __tablename__ = "userperm"
    id_user = db.Column(db.Integer, db.ForeignKey("user.id_user"), primary_key=True)
    id_permission = db.Column(db.Integer, db.ForeignKey("perm.id_permission"), primary_key=True)
    user = db.relationship("User")