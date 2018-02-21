from ws import db
from model import Permiso

from Organizacion import *

UsuPerm = db.Table('UsuPerm', db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id_usuario'), primary_key=True), db.Column('id_permiso', db.Integer, db.ForeignKey('permiso.id_permiso'), primary_key=True))


class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    apellidos = db.Column(db.String(255))
    permisos = db.relationship('Permiso', secondary=UsuPerm, lazy='subquery',backref=db.backref('permisos', lazy='dynamic'))

    def __init__(self, nombre='', apellidos='', id_organizacion=0):
        self.nombre = nombre
        self.apellidos = apellidos


    def get_usuario(self, id):
        usuario = Usuario.query.filter_by(id_usuario=id).first()
        return usuario


    def get_ult_usuario(self):
        usuarios = Usuario.query.all()

        numOrg = len(usuarios)
        usuario = usuarios[numOrg - 1]

        return usuario

    def get_usuario_organizaciones(self, usuario_id):

        ids = db.session.query(OrgUsu).filter_by(id_usuario=usuario_id)
        organizaciones=[]

        for id in ids:
            organizaciones.append(Organizacion().get_organizacion(id.id_organizacion))

        return organizaciones

    def post_usuario(self):
        db.session.add(self)
        db.session.commit()


    def put_usuario(self, nombre, apellidos):
        self.nombre = nombre
        self.apellidos = apellidos
        db.session.commit()

    def put_usuario_permisos(self, permiso):
        self.permisos.append(permiso)
        db.session.commit()

    def delete_usuario(self):
        db.session.delete(self)
        db.session.commit()

    def existe_usuario_permiso(self, id_permiso):
        for permiso in self.permisos:
            if(permiso.id_permiso==id_permiso):

                return True
        return False

    def delete_usuario_permiso(self, permiso):
        self.permisos.remove(permiso)
        db.session.commit()

    def get_permiso_usuarios(self, peticion_id):

        ids = db.session.query(UsuPerm).filter_by(id_permiso=peticion_id)
        usuarios=[]

        for id in ids:
            usuarios.append(Usuario().get_usuario(id.id_usuario))

        return usuarios



