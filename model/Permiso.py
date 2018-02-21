from ws import db

class Permiso(db.Model):
    id_permiso = db.Column(db.Integer, primary_key=True)
    id_tipoPermiso = db.Column(db.Integer)
    id_organizacion = db.Column(db.Integer)
    id_ecoe = db.Column(db.Integer)
    id_estacion = db.Column(db.Integer)

    def __init__(self, id_tipoPermiso=0, id_organizacion=0, id_ecoe=0, id_estacion=0):
        self.id_tipoPermiso = id_tipoPermiso
        self.id_organizacion = id_organizacion
        self.id_ecoe = id_ecoe
        self.id_estacion = id_estacion

    def get_permiso(self, id):
        permiso = Permiso.query.filter_by(id_permiso=id).first()
        return permiso

    def get_ult_permiso(self):
        permisos = Permiso.query.all()

        numPerm = len(permisos)
        permiso = permisos[numPerm - 1]

        return permiso

    def post_permiso(self):
        db.session.add(self)
        db.session.commit()



    #Edita el tipo de permiso.
    def put_permiso(self, id_tipoPermiso, id_organizacion, id_ecoe, id_estacion):
        self.id_tipoPermiso = id_tipoPermiso
        self.id_organizacion = id_organizacion
        self.id_ecoe = id_ecoe
        self.id_estacion = id_estacion

        db.session.commit()


    def delete_permiso(self):
        db.session.delete(self)
        db.session.commit()


