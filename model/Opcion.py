from ws import db

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

    def get_ult_opcion(self):
        opciones = Opcion.query.all()

        numopciones = len(opciones)
        opcion = opciones[numopciones-1]

        return opcion


    def post_opcion(self):
        db.session.add(self)
        db.session.commit()

    def put_opcion(self, puntos, descripcion):
        self.puntos = puntos
        self.descripcion = descripcion
        db.session.commit()

    def delete_opcion(self):
        db.session.delete(self)
        db.session.commit()
