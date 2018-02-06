from db import db

class Rueda(db.Model):
    cod_rueda = db.Column(db.String(255), primary_key=True)
    descripcion = db.Column(db.String(500))

    # TODO hacer que alumnos sea relationship
    alumnos = db.Column(db.Integer)

    def __init__(self, descripcion, alumnos):
        self.descripcion = descripcion
        self.alumnos = alumnos

    def get_rueda(self, cod):
        rueda = Rueda.query.filter_by(cod_rueda=cod).first()
        return rueda

    def post_rueda(self):
        db.session.add(self)
        db.session.commit()

    def put_rueda(self, descripcion):
        self.descripcion = descripcion
        db.session.commit()

    def delete_rueda(self):
        db.session.delete(self)
        db.session.commit()

    #TODO faltan los métodos relacionados con Rueda