from db import db


class Dia(db.Model):
    cod_dia = db.Column(db.String(255), primary_key=True)
    fecha = db.Column(db.Integer)

    # TODO hacer que turnos sea relationship
    turnos = db.Column(db.Integer)


    def __init__(self, fecha, turnos):
        self.fecha = fecha
        self.turnos = turnos

    def get_dia(self, cod):
        dia = Dia.query.filter_by(cod_dia=cod).first()
        return dia

    def post_dia(self):
        db.session.add(self)
        db.session.commit()

    def put_dia(self, fecha):
        self.fecha = fecha
        db.session.commit()

    def delete_dia(self):
        db.session.delete(self)
        db.session.commit()

    #TODO faltan los métodos relacionados con Turno