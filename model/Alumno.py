from ws import db

class Alumno(db.Model):
    id_alumno = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    dni = db.Column(db.String(25))
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ECOE.id'))
    id_rueda = db.Column(db.Integer, db.ForeignKey('rueda.id_rueda'))

    def __init__(self, nombre='', dni='', id_ecoe=0):
        self.nombre = nombre
        self.dni = dni
        self.id_ecoe = id_ecoe

    def get_alumno(self, id):
        alumno = Alumno.query.filter_by(id_alumno=id).first()
        return alumno

    def post_alumno(self):
        db.session.add(self)
        db.session.commit()

    def put_alumno(self, nombre, dni, id_ecoe):
        self.dni = dni
        self.nombre = nombre
        self.id_ecoe = id_ecoe
        db.session.commit()

    def put_alumno_id_rueda(self, id_rueda):
        self.id_rueda = id_rueda

        db.session.commit()

    def delete_alumno(self):
        db.session.delete(self)
        db.session.commit()

    def delete_alumno_id_rueda(self):
        self.id_rueda = None
        db.session.commit()

    def get_ult_alumno(self):
        alumnos = Alumno.query.all()

        numAlumnos = len(alumnos)
        alumno = alumnos[numAlumnos-1]

        return alumno
