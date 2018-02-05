from db import db

class Permiso(db.Model):
    id_permiso = db.Column(db.Integer, primary_key=True)
    id_tipoPermiso = db.Column(db.Integer)
    id_organizacion = db.Column(db.Integer)
    id_ecoe = db.Column(db.Integer)
    id_estacion = db.Column(db.Integer)

    def __init__(self, id_tipoPermiso, id_organizacion, id_ecoe, id_estacion):
        self.id_tipoPermiso = id_tipoPermiso
        self.id_organizacion = id_organizacion
        self.id_ecoe = id_ecoe
        self.id_estacion = id_estacion

    def get_permiso(self, id):
        permiso = Permiso.query.filter_by(id_permiso=id).first()
        return permiso

    def post_permiso(self):
        permiso = Permiso(id_tipoPermiso=self.id_tipoPermiso)
        db.session.add(permiso)

        db.session.commit()
        return permiso

    #Edita el tipo de permiso.
    def put_permisoTipoPermiso(self, id_tipoPermiso):
        permiso = Permiso.query.filter_by(id_permiso=self.id_permiso).first()
        permiso.id_tipoPermiso = id_tipoPermiso
        db.session.commit()

        return permiso

    #Edita el id de la organizacion
    def put_permisoOrganizacion(self, id_organizacion):
        permiso = Permiso.query.filter_by(id_permiso=self.id_permiso).first()
        permiso.id_organizacion = id_organizacion
        db.session.commit()

        return permiso

    #Edita el id de la ecoe
    def put_permisoEcoe(self, id_ecoe):
        permiso = Permiso.query.filter_by(id_permiso=self.id_permiso).first()
        permiso.id_ecoe = id_ecoe
        db.session.commit()

        return permiso

    #Edita el id de la estacion
    def put_permisoEstacion(self, id_estacion):
        permiso = Permiso.query.filter_by(id_permiso=self.id_permiso).first()
        permiso.id_estacion = id_estacion
        db.session.commit()

        return permiso

    def delete_permiso(self):
        permiso = Permiso.query.filter_by(id_permiso=self.id_permiso).first()

        db.session.delete(permiso)
        db.session.commit()

        return "OK"