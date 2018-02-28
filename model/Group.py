from ws import db

class Group(db.Model):
    __tablename__ = "group"
    id_group = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    id_station = db.Column(db.Integer, db.ForeignKey('sta.id_station'))
    questions = db.relationship('ques', backref='questions', lazy='dynamic')


    def __init__(self, nombre='', preguntas='', id_estacion=0):
        self.name = nombre
        self.questions = preguntas
        self.id_station = id_estacion

    def get_grupo(self, id):
        grupo = Group.query.filter_by(id_grupo=id).first()
        return grupo

    def get_ult_grupo(self):
        grupos = Group.query.all()

        numGrupos = len(grupos)
        grupo = grupos[numGrupos-1]

        return grupo


    def post_grupo(self):
        db.session.add(self)
        db.session.commit()

    def put_grupo(self, nombre, id_estacion):
        self.name = nombre
        self.id_station=id_estacion
        db.session.commit()

    def delete_grupo(self):
        db.session.delete(self)
        db.session.commit()

    def existe_grupo_pregunta(self, id_pregunta):
        for pregunta in self.questions:
            if(pregunta.id_pregunta==id_pregunta):
                return True
        return False




