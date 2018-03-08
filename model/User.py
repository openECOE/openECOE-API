from ws import db
from model import Permission

from model import Organization
from .Organization import orguser

userperm = db.Table('userperm', db.Column('id_user', db.Integer, db.ForeignKey('user.id_user'), primary_key=True), db.Column('id_permission', db.Integer, db.ForeignKey('perm.id_permission'), primary_key=True))


class User(db.Model):
    __tablename__ = "user"
    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    permissions = db.relationship('Permission', secondary=userperm, lazy='subquery', backref=db.backref('perm', lazy='dynamic'))

    def __init__(self, name='', surname=''):
        self.name = name
        self.surname = surname


    def get_user(self, id):
        user = User.query.filter_by(id_user=id).first()
        return user


    def get_last_user(self):
        users = User.query.all()

        numOrg = len(users)
        user = users[numOrg - 1]

        return user

    def get_user_organizations(self, user_id):

        ids = db.session.query(orguser).filter_by(id_user=user_id)
        organizations=[]

        for id in ids:
            organizations.append(Organization().get_organization(id.id_organization))

        return organizations

    def post_user(self):
        db.session.add(self)
        db.session.commit()


    def put_user(self, name, surname):
        self.name = name
        self.surname = surname
        db.session.commit()

    def put_user_permission(self, permission):
        self.permissions.append(permission)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    def exist_user_permission(self, id_permission):
        for permission in self.permissions:
            if(permission.id_permiso==id_permission):

                return True
        return False

    def delete_user_permission(self, permission):
        self.permissions.remove(permission)
        db.session.commit()

    def get_permission_users(self, permission_id):

        ids = db.session.query(userperm).filter_by(id_permission=permission_id)
        user=[]

        for id in ids:
            user.append(User().get_user(id.id_usuario))

        return user



