from db import db

class Grupo(db.Model):
    id_grupo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))

    # TODO hacer que preguntas sea relationship
    preguntas = db.Column(db.Integer)

    def __init__(self, nombre, preguntas):
        self.nombre = nombre
        self.preguntas = preguntas

    def get_grupo(self, id):
        grupo = Grupo.query.filter_by(id_grupos=id).first()
        return grupo

    def post_grupo(self):
        db.session.add(self)
        db.session.commit()

    def put_grupo(self, nombre):
        self.nombre = nombre
        db.session.commit()

    def delete_grupo(self):
        db.session.delete(self)
        db.session.commit()

    #TODO faltan los métodos relacionados con Preguntas