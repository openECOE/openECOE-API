from db import db

class Alarma(db.Model):
    id_alarma = db.Column(db.Integer, primary_key=True)
    tiempo = db.Column(db.Integer)
    sonido = db.Column(db.String(500))

    def __init__(self, tiempo, sonido):
        self.tiempo = tiempo
        self.sonido = sonido

    def get_alarma(self, id):
        alarma = Alarma.query.filter_by(id_alarma = id).first()
        return alarma

    def post_alarma(self):
        db.session.add(self)
        db.session.commit()

    def put_alarmaTiempo(self, tiempo):
        self.tiempo = tiempo
        db.session.commit()

    def put_alarmaSonido(self, sonido):
        self.sonido = sonido
        db.session.commit()

    def delete_alarma(self):
        db.session.delete(self)
        db.session.commit()