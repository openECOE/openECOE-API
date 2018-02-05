from db import db

class Alumno:
    id_alumno = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    dni = db.Column(db.String(25))
  #  id_ecoe = db.Column(db.Integer, db.ForeignKey('ECOE.id'))

    def __init__(self, id_alumno='', nombre='', DNI='', id_ecoe=0):
        self.nombre = nombre
        self.DNI = DNI
   #     self.id_ecoe = id_ecoe

    def __repr__(self):
        return '<Alumno %r>' %self.nombre


