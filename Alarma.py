from db import db

class Alarma(db.Model):
    id_alarma = db.Column(db.Integer, primary_key=True)
    tiempo = db.Column(db.Integer)
    sonido = db.Column(db.String(550))
    id_cronometro = db.Column(db.Integer, db.ForeignKey('cronometro.id_cronometro'))

    def __init__(self, tiempo=0, sonido='', id_cronometro=0):
        self.tiempo = tiempo
        self.sonido = sonido
        self.id_cronometro = id_cronometro

    def get_alarma(self, id):
        alarma = Alarma.query.filter_by(id_alarma = id).first()
        return alarma

    def get_ult_alarma(self):
        alarmas = Alarma.query.all()

        numAlarmas = len(alarmas)
        alarma = alarmas[numAlarmas - 1]

        return alarma

    def post_alarma(self):
        db.session.add(self)
        db.session.commit()


    def put_alarma(self, tiempo, sonido, id_cronometro):
        self.tiempo = tiempo
        self.sonido = sonido
        self.id_cronometro = id_cronometro
        db.session.commit()


    def delete_alarma(self):
        db.session.delete(self)
        db.session.commit()