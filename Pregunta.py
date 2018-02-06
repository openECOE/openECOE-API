from db import db

class Pregunta(db.Model):
    id_pregunta = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.String(255))
    tipo_opcion = db.Column(db.Integer)

    # TODO hacer que area y opcion sea relationship
    area_pregunta = db.Column(db.Integer)
    opciones = db.Column(db.Integer)

    def __init__(self, referencia, tipo_opcion, area_pregunta, opciones):
        self.referencia = referencia
        self.tipo_opcion = tipo_opcion
        self.area_pregunta = area_pregunta
        self.opciones = opciones

    def get_pregunta(self, id):
        pregunta = Pregunta.query.filter_by(id_pregunta=id).first()
        return pregunta

    def post_pregunta(self):
        db.session.add(self)
        db.session.commit()

    #Edita la ref de preguntas
    def put_preguntaRef(self, ref):
        self.ref = ref
        db.session.commit()

    # Edita el tipo de opción de preguntas
    def put_preguntaTipoOpcion(self, tipo_opcion):
        self.tipo_opcion = tipo_opcion
        db.session.commit()

    def delete_pregunta(self):
        db.session.delete(self)
        db.session.commit()

    #TODO faltan los métodos relacionados con Area y Opción