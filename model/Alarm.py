from ws import db

class Alarm(db.Model):
    __tablename__= "ala"

    id_alarm = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    sound = db.Column(db.String(550))
    id_chronometer = db.Column(db.Integer, db.ForeignKey('chro.id_chronometer'))

    def __init__(self, tiempo=0, sonido='', id_cronometro=0):
        self.time = tiempo
        self.sound = sonido
        self.id_chronometer = id_cronometro

    def get_alarma(self, id):
        alarma = Alarm.query.filter_by(id_alarma = id).first()
        return alarma

    def get_ult_alarma(self):
        alarmas = Alarm.query.all()

        numAlarmas = len(alarmas)
        alarma = alarmas[numAlarmas - 1]

        return alarma

    def post_alarma(self):
        db.session.add(self)
        db.session.commit()

    def put_alarma(self, tiempo, sonido, id_cronometro):
        self.time = tiempo
        self.sound = sonido
        self.id_chronometer = id_cronometro
        db.session.commit()


    def delete_alarma(self):
        db.session.delete(self)
        db.session.commit()

