from db import db

class Cronometro(db.Model):
    id_cronometro = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    tiempo_total = db.Column(db.Integer)

    # TODO hacer que alarmas sea relationship
    alarmas = db.Column(db.Integer)

    def __init__(self, nombre, tiempo_total, alarmas):
        self.nombre = nombre
        self.tiempo_total = tiempo_total
        self.alarmas = alarmas

    def get_cronometro(self, id):
        cronometro = Cronometro.query.filter_by(id_cronometro=id).first()
        return cronometro

    def post_cronometro(self):
        db.session.add(self)
        db.session.commit()

    def put_cronometroNombre(self, nombre):
        self.nombre = nombre
        db.session.commit()

    def put_cronometroTiempoTotal(self, tiempo_total):
        self.tiempo_total = tiempo_total
        db.session.commit()

    def delete_cronometro(self):
        db.session.delete(self)
        db.session.commit()

    #TODO faltan los métodos relacionados con alarma