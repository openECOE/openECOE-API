from db import db

class Turno(db.Model):
    cod_turno = db.Column(db.String(255), primary_key=True)
    hora_inicio = db.Column(db.Integer)

    # TODO hacer que ruedas sea relationship
    ruedas = db.Column(db.Integer)

    def __init__(self, hora_inicio, ruedas):
        self.hora_inicio = hora_inicio
        self.ruedas = ruedas

    def get_turno(self, cod):
        turno = Turno.query.filter_by(cod_turno = cod).first()
        return turno

    def post_turno(self):
        db.session.add(self)
        db.session.commit()

    def put_turno(self, hora_inicio):
        self.hora_inicio = hora_inicio
        db.session.commit()


    def delete_turno(self):
        db.session.delete(self)
        db.session.commit()


    #TODO faltan los métodos relacionados con Rueda