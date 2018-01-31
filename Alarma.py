from db import db

class Alarma(db.Model):
    id_alarma = db.Column(db.Integer, primary_key=True)
    tiempo = db.Column(db.Integer)
    sonido = db.Column(db.String(500))

    def __init__(self, tiempo, sonido):
        self.tiempo = tiempo
        self.sonido = sonido

    def __repr__(self):
        return '<Sonido %r>' %self.sonido

    def post_alarma(self):
        alarma = Alarma(self.tiempo, self.sonido)

        db.session.add(alarma)
        db.session.commit()