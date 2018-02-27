from  ws import db
from model import Alarma

CronoEst = db.Table('CronoEst', db.Column('id_cronometro', db.Integer, db.ForeignKey('cronometro.id_cronometro'), primary_key=True), db.Column('id_estacion', db.Integer, db.ForeignKey('estacion.id_estacion'), primary_key=True))

class Cronometro(db.Model):
    id_cronometro = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    tiempo_total = db.Column(db.Integer)
    alarmas = db.relationship('Alarma', backref='alarmas', lazy='dynamic')



    def __init__(self, nombre='', tiempo_total=0):
        self.nombre = nombre
        self.tiempo_total = tiempo_total

    def get_cronometro(self, id):
        cronometro = Cronometro.query.filter_by(id_cronometro=id).first()
        return cronometro

    def get_ult_cronometro(self):
        cronometros = Cronometro.query.all()

        numCronometros = len(cronometros)
        cronometro = cronometros[numCronometros - 1]

        return cronometro


    def post_cronometro(self):
        db.session.add(self)
        db.session.commit()

    def put_cronometro(self, nombre, tiempo_total):
        self.nombre = nombre
        self.tiempo_total = tiempo_total

        db.session.commit()


    def delete_cronometro(self):
        db.session.delete(self)
        db.session.commit()


    def existe_cronometro_alarma(self, id_alarma):
        for alarma in self.alarmas:
            if(alarma.id_alarma==id_alarma):
                return True
        return False

