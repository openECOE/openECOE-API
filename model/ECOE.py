from ws import db
from model import Cronometro

class ECOE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    areas = db.relationship('Area', backref='areas', lazy='dynamic')
    alumnos = db.relationship('Alumno', backref='alumnos', lazy='dynamic')
    estaciones = db.relationship('Estacion', backref='estaciones', lazy='dynamic')
    dias = db.relationship('Dia', backref='dias', lazy='dynamic')
    #cronometros = db.relationship('Cronometro', backref='cronometros', lazy='dynamic')
    id_organizacion = db.Column(db.Integer, db.ForeignKey('organizacion.id_organizacion'))

    def __init__(self, nombre='', id_organizacion=0):
        self.nombre = nombre
        self.id_organizacion = id_organizacion

    def __repr__(self):
        return '<ECOE %r>' %self.nombre

    #def get_ECOEs_id(self):
     #   ids = ECOE.query.with_entities(ECOE.id).all()
     #   return list(np.squeeze(ids))

    def get_ECOE(self, id):
        ecoe = ECOE.query.filter_by(id=id).first()
        return ecoe;

    def get_ult_ecoe(self):
        ecoes = ECOE.query.all()

        numEcoes = len(ecoes)
        ecoe = ecoes[numEcoes-1]

        return ecoe


    def post_ecoe(self):
        db.session.add(self)
        db.session.commit()

    def put_ecoe(self, nombre, id_organizacion):
        self.nombre = nombre
        self.id_organizacion = id_organizacion
        db.session.commit()


    def delete_ecoe(self):
        db.session.delete(self)
        db.session.commit()

    def existe_ecoe_area(self, id_area):
        for area in self.areas:
            if(area.id_area==id_area):
                return True
        return False

    def existe_ecoe_alumno(self, id_alumno):
        for alumno in self.alumnos:
            if(alumno.id_alumno==id_alumno):
                return True
        return False

    def existe_ecoe_estacion(self, id_estacion):
        for estacion in self.estaciones:
            if(estacion.id_estacion==id_estacion):
                return True
        return False





