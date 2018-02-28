from ws import db
from model import Student

class Round(db.Model):
    __tablename__="round"

    id_round = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    id_shift = db.Column(db.Integer, db.ForeignKey('shi.id_shift'))
    students = db.relationship('Student', backref='studentsRound', lazy='dynamic')

    def __init__(self, descripcion="", id_turno=0):
        self.description = descripcion
        self.id_shift = id_turno

    def get_rueda(self, id):
        rueda = Round.query.filter_by(id_rueda=id).first()
        return rueda

    def get_ult_rueda(self):
        ruedas = Round.query.all()

        numruedas = len(ruedas)
        rueda = ruedas[numruedas-1]

        return rueda

    def post_rueda(self):
        db.session.add(self)
        db.session.commit()

    def put_rueda(self, descripcion, id_turno):
        self.description = descripcion
        self.id_shift = id_turno

        db.session.commit()

    def delete_rueda(self):
        db.session.delete(self)
        db.session.commit()

    def existe_rueda_alumno(self, id_alumno):
        for alumno in self.students:
            if(alumno.id_alumno==id_alumno):
                return True
        return False


