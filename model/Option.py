from ws import db

class Option(db.Model):
    __tablename__ = "opt"

    id_option = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Integer)
    description = db.Column(db.String(255))
    id_questions = db.Column(db.Integer, db.ForeignKey('ques.id_question'))


    def __init__(self, puntos=0, descripcion='', id_pregunta=0):
        self.puntos = puntos
        self.description = descripcion
        self.id_questions = id_pregunta

    def get_opcion(self, id):
        opcion = Option.query.filter_by(id_opcion=id).first()
        return opcion

    def get_ult_opcion(self):
        opciones = Option.query.all()

        numopciones = len(opciones)
        opcion = opciones[numopciones-1]

        return opcion


    def post_opcion(self):
        db.session.add(self)
        db.session.commit()

    def put_opcion(self, puntos, descripcion, id_pregunta):
        self.puntos = puntos
        self.description = descripcion
        self.id_questions = id_pregunta

        db.session.commit()

    def delete_opcion(self):
        db.session.delete(self)
        db.session.commit()
