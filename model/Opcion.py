from ws import db

class Opcion(db.Model):
    id_opcion = db.Column(db.Integer, primary_key=True)
    puntos = db.Column(db.Integer)
    descripcion = db.Column(db.String(255))
    id_pregunta = db.Column(db.Integer, db.ForeignKey('pregunta.id_pregunta'))


    def __init__(self, puntos=0, descripcion='', id_pregunta=0):
        self.puntos = puntos
        self.descripcion = descripcion
        self.id_pregunta = id_pregunta

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

    def put_opcion(self, puntos, descripcion, id_pregunta):
        self.puntos = puntos
        self.descripcion = descripcion
        self.id_pregunta = id_pregunta

        db.session.commit()

    def delete_opcion(self):
        db.session.delete(self)
        db.session.commit()
