from ws import *

class Turno(db.Model):
    id_turno = db.Column(db.Integer, primary_key=True)
    hora_inicio = db.Column(db.Integer)
    id_dia = db.Column(db.Integer, db.ForeignKey('dia.id_dia'))
    ruedas = db.relationship('Rueda', backref='ruedas', lazy='dynamic')

    def __init__(self, hora_inicio, ruedas):
        self.hora_inicio = hora_inicio
        self.ruedas = ruedas

    def get_turno(self, id):
        turno = Turno.query.filter_by(id_turno = id).first()
        return turno

    def get_ult_turno(self):
        turnos = Turno.query.all()

        numturnos = len(turnos)
        turno = turnos[numturnos-1]

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

