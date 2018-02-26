from ws import db

class Rueda(db.Model):
    id_rueda = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(500))
    id_turno = db.Column(db.Integer, db.ForeignKey('turno.id_turno'))

    def __init__(self, descripcion="", id_turno=0):
        self.descripcion = descripcion
        self.id_turno = id_turno

    def get_rueda(self, id):
        rueda = Rueda.query.filter_by(id_rueda=id).first()
        return rueda

    def get_ult_rueda(self):
        ruedas = Rueda.query.all()

        numruedas = len(ruedas)
        rueda = ruedas[numruedas-1]

        return rueda

    def post_rueda(self):
        db.session.add(self)
        db.session.commit()

    def put_rueda(self, descripcion, id_turno):
        self.descripcion = descripcion
        self.id_turno = id_turno

        db.session.commit()

    def delete_rueda(self):
        db.session.delete(self)
        db.session.commit()


