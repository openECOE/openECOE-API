from ws import db

class Permission(db.Model):
    __tablename__ = "perm"
    id_permission = db.Column(db.Integer, primary_key=True)
    id_typePermission = db.Column(db.Integer)
    id_organization = db.Column(db.Integer)
    id_ecoe = db.Column(db.Integer)
    id_station = db.Column(db.Integer)

    def __init__(self, id_typePermission=0, id_organization=0, id_ecoe=0, id_station=0):
        self.id_typePermission = id_typePermission
        self.id_organization = id_organization
        self.id_ecoe = id_ecoe
        self.id_station = id_station

    def get_permission(self, id):
        permission = Permission.query.filter_by(id_permission=id).first()
        return permission

    def get_last_permission(self):
        permissions = Permission.query.all()

        numPerm = len(permissions)
        permission = permissions[numPerm - 1]

        return permission

    def post_permission(self):
        db.session.add(self)
        db.session.commit()



    #Edita el tipo de permiso.
    def put_permission(self, id_typePermission, id_organization, id_ecoe, id_station):
        self.id_typePermission = id_typePermission
        self.id_organization = id_organization
        self.id_ecoe = id_ecoe
        self.id_station = id_station

        db.session.commit()


    def delete_permission(self):
        db.session.delete(self)
        db.session.commit()


