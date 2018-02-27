from ws import db
from model import Area, Alumno, Estacion, Dia, Cronometro

ecoeCrono = db.Table('ecoeCrono', db.Column('id_ecoe', db.Integer, db.ForeignKey('ECOE.id'), primary_key=True), db.Column('id_cronometro', db.Integer, db.ForeignKey('cronometro.id_cronometro'), primary_key=True))

class ECOE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    areas = db.relationship('Area', backref='areas', lazy='dynamic')
    alumnos = db.relationship('Alumno', backref='alumnos', lazy='dynamic')
    cronometros = db.relationship('Cronometro', secondary=ecoeCrono, lazy='subquery', backref=db.backref('ecoesCro', lazy='dynamic'))
    estaciones = db.relationship('Estacion', backref='estaciones', lazy='dynamic')
    dias = db.relationship('Dia', backref='dias', lazy='dynamic')
    id_organizacion = db.Column(db.Integer, db.ForeignKey('organizacion.id_organizacion'))

    def __init__(self, nombre='', id_organizacion=0):
        self.nombre = nombre
        self.id_organizacion = id_organizacion

    def __repr__(self):
        return '<ECOE %r>' %self.nombre

    #def get_ECOEs_id(self):
     #   ids = ECOE.query.with_entities(ECOE.id).all()
     #   return list(np.squeeze(ids))

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

    def put_ecoe(self, nombre, id_organizacion):
        self.nombre = nombre
        self.id_organizacion = id_organizacion
        db.session.commit()


    def delete_ecoe(self):
        db.session.delete(self)
        db.session.commit()


    def existe_ecoe_alumno(self, id_alumno):
        for alumno in self.alumnos:
            if(alumno.id_alumno==id_alumno):
                return True
        return False

    def existe_ecoe_estacion(self, id_estacion):
        for estacion in self.estaciones:
            if(estacion.id_estacion==id_estacion):
                return True
        return False

    def existe_ecoe_cronometro(self, id_cronometro):
        for cronometro in self.cronometros:
            if(cronometro.id_cronometro==id_cronometro):
                return True
        return False

    def existe_ecoe_dias(self, id_dia):
        for dia in self.dias:
            if(dia.id_dia == id_dia):
                return True
        return False

    def put_ecoe_cronometro(self, cronometro):
        self.cronometros.append(cronometro)
        db.session.commit()

    def delete_ecoe_cronometro(self, cronometro):
        self.cronometros.remove(cronometro)
        db.session.commit()



