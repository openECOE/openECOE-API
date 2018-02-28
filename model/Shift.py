from ws import *

class Shift(db.Model):
    __tablename__="shi"

    id_shift = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.TIME)
    id_day = db.Column(db.Integer, db.ForeignKey('day.id_day'))
    rounds = db.relationship('Round', backref='rounds', lazy='dynamic')

    def __init__(self, hora_inicio="00:00", id_dia=0):
        self.start_time = hora_inicio
        self.id_day = id_dia

    def get_turno(self, id):
        turno = Shift.query.filter_by(id_turno = id).first()
        return turno

    def get_ult_turno(self):
        turnos = Shift.query.all()

        numturnos = len(turnos)
        turno = turnos[numturnos-1]

        return turno

    def post_turno(self):
        db.session.add(self)
        db.session.commit()

    def put_turno(self, hora_inicio="00:00", id_dia=0):
        self.start_time = hora_inicio
        self.id_day = id_dia

        db.session.commit()


    def delete_turno(self):
        db.session.delete(self)
        db.session.commit()

    def existe_turno_rueda(self, id_rueda):
        for rueda in self.rounds:
            if(rueda.id_rueda == id_rueda):
                return True
        return False