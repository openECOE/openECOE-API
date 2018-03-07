from  ws import db
from model import Alarm

class Chronometer(db.Model):
    __tablename__ = "chro"

    id_chronometer = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    total_time = db.Column(db.Integer)
    alarms = db.relationship('Alarm', backref='alarmas', lazy='dynamic')

    def __init__(self, nombre='', tiempo_total=0):
        self.name = nombre
        self.total_time = tiempo_total

    def get_cronometro(self, id):
        cronometro = Chronometer.query.filter_by(id_cronometro=id).first()
        return cronometro

    def get_ult_cronometro(self):
        cronometros = Chronometer.query.all()

        numCronometros = len(cronometros)
        cronometro = cronometros[numCronometros - 1]

        return cronometro


    def post_cronometro(self):
        db.session.add(self)
        db.session.commit()

    def put_cronometro(self, nombre, tiempo_total):
        self.name = nombre
        self.total_time = tiempo_total

        db.session.commit()


    def delete_cronometro(self):
        db.session.delete(self)
        db.session.commit()


    def existe_cronometro_alarma(self, id_alarma):
        for alarma in self.alarms:
            if(alarma.id_alarma==id_alarma):
                return True
        return False

