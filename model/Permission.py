from ws import db

class Permission(db.Model):
    __tablename__ = "perm"
    id_permission = db.Column(db.Integer, primary_key=True)
    id_typePermission = db.Column(db.Integer)
    id_organization = db.Column(db.Integer)
    id_ecoe = db.Column(db.Integer)
    id_station = db.Column(db.Integer)


