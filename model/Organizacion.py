from ws import db
from model import Usuario
from ECOE import ECOE

OrgUsu = db.Table('OrgUsu', db.Column('id_organizacion', db.Integer, db.ForeignKey('organizacion.id_organizacion'), primary_key=True), db.Column('id_usuario', db.Integer, db.ForeignKey('usuario.id_usuario'), primary_key=True))


class Organizacion(db.Model):
    id_organizacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    usuarios = db.relationship('Usuario', secondary=OrgUsu, lazy ='subquery', backref=db.backref('usuarios', lazy = 'dynamic'))
    ecoes = db.relationship('ECOE', backref='ecoes', lazy='dynamic')

    def __init__(self, nombre=''):
        self.nombre = nombre

    #def get_organizacion_ids(self):
     #   ids = Organizacion.query.with_entities(Organizacion.id_organizacion).all()
      #  return list(np.squeeze(ids))

    def get_usuario_organizaciones(self, usuario_id):

        ids = db.session.query(OrgUsu).filter_by(id_usuario=usuario_id)
        organizaciones=[]

        for id in ids:
            organizaciones.append(Organizacion().get_organizacion(id.id_organizacion))

        return organizaciones

    def get_organizacion(self, id):
        organizacion = Organizacion.query.filter_by(id_organizacion=id).first()
        return organizacion

    def get_ult_organizacion(self):
        organizaciones = Organizacion.query.all()

        numOrg = len(organizaciones)
        organizacion = organizaciones[numOrg - 1]

        return organizacion

    def post_organizacion(self):
        db.session.add(self)
        db.session.commit()


    def put_organizacion(self, nombre):
        self.nombre = nombre
        db.session.commit()

    def delete_organizacion(self):
        db.session.delete(self)
        db.session.commit()

    def existe_organizacion_usuario(self, id_usuario):
        for usuario in self.usuarios:
            if(usuario.id_usuario==id_usuario):
                return True
        return False


    def put_organizacion_usuario(self, usuario):
        self.usuarios.append(usuario)
        db.session.commit()


    def delete_organizacion_usuario(self, usuario):
        self.usuarios.remove(usuario)
        db.session.commit()

    def get_usuario_organizaciones(self, usuario_id):

        ids = db.session.query(OrgUsu).filter_by(id_usuario=usuario_id)
        organizaciones=[]

        for id in ids:
            organizaciones.append(Organizacion().get_organizacion(id.id_organizacion))

        return organizaciones

    def existe_organizacion_ecoe(self, id_ecoe):
        for ecoe in self.ecoes:
            if(ecoe.id==id_ecoe):
                return True
        return False

