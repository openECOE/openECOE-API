from ws import db
from model import Area, Opcion

class Pregunta(db.Model):
    id_pregunta = db.Column(db.Integer, primary_key=True)
    id_grupo = db.Column(db.Integer, db.ForeignKey('grupo.id_grupo'))
    id_area = db.Column(db.Integer, db.ForeignKey('area.id_area'))
    area = db.relationship('Area', backref='area')
    ref = db.Column(db.String(255))
    tipo_opcion = db.Column(db.String(500))
    opciones = db.relationship('Opcion', backref='opciones', lazy='dynamic')

    def __init__(self, referencia='', tipo_opcion='', id_grupo=0):
        self.ref = referencia
        self.tipo_opcion = tipo_opcion
        self.id_grupo = id_grupo

    def get_pregunta(self, id):
        pregunta = Pregunta.query.filter_by(id_pregunta=id).first()
        return pregunta

    def get_ult_pregunta(self):
        preguntas = Pregunta.query.all()

        numpreguntas = len(preguntas)
        pregunta = preguntas[numpreguntas-1]

        return pregunta

    def post_pregunta(self):
        db.session.add(self)
        db.session.commit()

    def post_pregunta_area(self, area):
        self.area = area
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

    def existe_pregunta_id_ecoe(self, id_area):
        return True

        area = Area().get_area(id_area)

        if(area):
            id_ecoe_new = area.id_ecoe

            grupo = Grupo().get_grupo(self.id_grupo)
            estacion = Estacion().get_estacion(grupo.id_estacion)
            id_ecoe_old = estacion.id_ecoe

            if(id_ecoe_new==id_ecoe_old):
                return True
            else:
                return False

        else:
            return False

    def existe_pregunta_opcion(self, id_opcion):
        for opcion in self.opciones:
            if(opcion.id_opcion==id_opcion):
                return True
        return False

    def put_pregunta_area(self, id_area):
        self.id_area = id_area
        db.session.commit()

    def delete_pregunta_area(self):
        self.id_area = None
        db.session.commit()





