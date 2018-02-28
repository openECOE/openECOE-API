from ws import db
from model import Area, Student, Station, Day, Chronometer

ecoechro = db.Table('ecoechro', db.Column('id_ecoe', db.Integer, db.ForeignKey('ecoe.id'), primary_key=True), db.Column('id_chronometer', db.Integer, db.ForeignKey('chro.id_chronometer'), primary_key=True))

class ECOE(db.Model):
    __tablename__ = "ecoe"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    areas = db.relationship('Area', backref='areas', lazy='dynamic')
    students = db.relationship('Alumno', backref='alumnos', lazy='dynamic')
    chronometers = db.relationship('Cronometro', secondary=ecoechro, lazy='subquery', backref=db.backref('ecoesCro', lazy='dynamic'))
    stations = db.relationship('Estacion', backref='estaciones', lazy='dynamic')
    days = db.relationship('Dia', backref='dias', lazy='dynamic')
    id_organization = db.Column(db.Integer, db.ForeignKey('org.id_organization'))

    def __init__(self, name='', id_organization=0):
        self.name = name
        self.id_organization = id_organization

    def get_ECOE(self, id):
        ecoe = ECOE.query.filter_by(id=id).first()
        return ecoe;

    def get_ult_ecoe(self):
        ecoes = ECOE.query.all()

        numEcoes = len(ecoes)
        ecoe = ecoes[numEcoes-1]

        return ecoe


    def post_ecoe(self):
        db.session.add(self)
        db.session.commit()

    def put_ecoe(self, name, id_organization):
        self.name = name
        self.id_organization = id_organization
        db.session.commit()


    def delete_ecoe(self):
        db.session.delete(self)
        db.session.commit()


    def exists_ecoe_chronometer(self, id_chronometer):
        for chronometer in self.chronometers:
            if(chronometer.id_chronometer==id_chronometer):
                return True
        return False


    def put_ecoe_chronometer(self, cronometro):
        self.chronometers.append(cronometro)
        db.session.commit()

    def delete_ecoe_chronometer(self, cronometro):
        self.chronometers.remove(cronometro)
        db.session.commit()



