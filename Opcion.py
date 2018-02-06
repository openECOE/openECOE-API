from db import db

class Opcion(db.Model):
    id_opcion = db.Column(db.Integer, primary_key=True)
    puntos = db.Column(db.Integer)
    descripcion = db.Column(db.String(255))

    def __init__(self, puntos, descripcion):
        self.puntos = puntos
        self.descripcion = descripcion

    def get_opcion(self, id):
        opcion = Opcion.query.filter_by(id_opcion=id).first()
        return opcion

    def post_opcion(self):
        db.session.add(self)
        db.session.commit()

    #Edita puntos de opcion
    def put_opcionPuntos(self, puntos):
        self.puntos = puntos
        db.session.commit()

    #Edita descripcion de opcion
    def put_opcionDescripcion(self, descripcion):
        self.descripcion = descripcion
        db.session.commit()

    def delete_opcion(self):
        db.session.delete(self)
        db.session.commit()

