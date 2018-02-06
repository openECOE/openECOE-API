from db import db


class Dia(db.Model):
    cod_dia = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Integer)

    # TODO hacer que turnos sea relationship
    turnos = db.Column(db.Integer)


    def __init__(self, fecha, turnos):
        self.cod_dia = cod_dia
        self.fecha = fecha
        self.turnos = turnos

    def get_dia(self, cod):
        dia = Dia.query.filter_by(cod_dia=cod).first()
        return dia

    def post_dia(self):
        dia = Dia(cod_dia=self.cod_dia)
        db.session.add(dia)

        db.session.commit()
        return dia

    def put_dia(self, cod_dia):
        dia = Dia.query.filter_by(cod_dia=self.cod_dia).first()
        dia.fecha = fecha
        db.session.commit()

        return dia

    def delete_dia(self):
        dia = Dia.query.filter_by(cod_dia=self.cod_dia).first()

        db.session.delete(dia)
        db.session.commit()

        return "OK"

    #TODO faltan los métodos relacionados con Turno