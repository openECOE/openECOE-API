from db import db

class Pregunta(db.Model):
    id_pregunta = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.String(500))
    tipo_pregunta = db.Column(db.String(255))
    id_grupo = db.Column(db.Integer, db.ForeignKey('grupo.id_grupo'))

    #area_pregunta = db.Column(db.Integer)
    #opciones = db.Column(db.Integer)

    def __init__(self, referencia='', tipo_pregunta='', id_grupo=0):
        self.ref = referencia
        self.tipo_pregunta = tipo_pregunta
        self.id_grupo = id_grupo

    def get_pregunta(self, id):
        pregunta = Pregunta.query.filter_by(id_pregunta=id).first()
        return pregunta

    def get_ult_pregunta(self):
        preguntas = Pregunta.query.all()

        numPreguntas = len(preguntas)
        pregunta = preguntas[numPreguntas - 1]

        return pregunta


    def post_pregunta(self):
        db.session.add(self)
        db.session.commit()

    #Edita la ref de preguntas
    def put_pregunta(self, ref, tipo_pregunta, id_grupo):
        self.ref = ref
        self.tipo_pregunta = tipo_pregunta
        self.id_grupo = id_grupo
        
        db.session.commit()

    def delete_pregunta(self):
        db.session.delete(self)
        db.session.commit()


#TODO Area