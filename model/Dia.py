from ws import db

class Dia(db.Model):
    id_dia = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Integer)
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ECOE.id'))
    turnos = db.relationship('Turno', backref='turnos', lazy='dynamic')

    def __init__(self, fecha, turnos):
        self.fecha = fecha
        self.turnos = turnos

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

    def put_dia(self, fecha):
        self.fecha = fecha
        db.session.commit()

    def delete_dia(self):
        db.session.delete(self)
        db.session.commit()

