from ws import db
from model import Question, Station

class Group(db.Model):
    __tablename__ = "group"
    id_group = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    id_station = db.Column(db.Integer, db.ForeignKey('sta.id_station'))
    questions = db.relationship('Question', backref='questions', lazy='dynamic')


    def __init__(self, name='', id_station=0):
        self.name = name
        self.id_station = id_station

    def get_group(self, id):
        group = Group.query.filter_by(id_grupo=id).first()
        return group

    def get_last_group(self):
        groups = Group.query.all()

        numGroups = len(groups)
        group = groups[numGroups-1]

        return group


    def post_group(self):
        db.session.add(self)
        db.session.commit()

    def put_group(self, name, id_station):
        self.name = name
        self.id_station=id_station
        db.session.commit()

    def delete_grupo(self):
        db.session.delete(self)
        db.session.commit()




