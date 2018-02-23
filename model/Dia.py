from ws import db, datetime

class Dia(db.Model):
    id_dia = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ECOE.id'))
    turnos = db.relationship('Turno', backref='turnos', lazy='dynamic')

    def __init__(self, fecha='', id_ecoe=0):
        self.fecha = fecha
        self.id_ecoe = id_ecoe

    def get_dia(self, id):
        dia = Dia.query.filter_by(id_dia=id).first()
        return dia

    def get_ult_dia(self):
        dias = Dia.query.all()

        numdias = len(dias)
        dia = dias[numdias-1]

        return dia

    def post_dia(self):
        db.session.add(self)
        db.session.commit()

    def put_dia(self, fecha, id_ecoe):

        self.fecha = fecha
        self.id_ecoe = id_ecoe

        db.session.commit()

    def delete_dia(self):
        db.session.delete(self)
        db.session.commit()

    def existe_dia_turno(self, id_turno):
        for turno in self.turnos:
            if(turno.id_turno == id_turno):
                return True
        return False
