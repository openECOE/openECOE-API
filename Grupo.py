from db import db



class Grupo(db.Model):
    id_grupo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    id_estacion = db.Column(db.Integer, db.ForeignKey('estacion.id_estacion'))

    preguntas = db.Column(db.Integer)

    def __init__(self, nombre='', preguntas='', id_estacion=0):
        self.nombre = nombre
        self.preguntas = preguntas
        self.id_estacion = id_estacion

    def get_grupo(self, id):
        grupo = Grupo.query.filter_by(id_grupo=id).first()
        return grupo

    def get_ult_grupo(self):
        grupos = Grupo.query.all()

        numGrupos = len(grupos)
        grupo = grupos[numGrupos-1]

        return grupo
        return grupo

    def post_grupo(self):
        db.session.add(self)
        db.session.commit()

    def put_grupo(self, nombre, id_estacion):
        self.nombre = nombre
        self.id_estacion=id_estacion
        db.session.commit()

    def delete_grupo(self):
        db.session.delete(self)
        db.session.commit()
