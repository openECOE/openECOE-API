from ws import db
from model import User, ECOE

orguser = db.Table('orguser', db.Column('id_organization', db.Integer, db.ForeignKey('org.id_organization'), primary_key=True), db.Column('id_user', db.Integer, db.ForeignKey('user.id_user'), primary_key=True))

class Organization(db.Model):
    __tablename__ = "org"
    id_organization = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    users = db.relationship('User', secondary=orguser, lazy ='subquery', backref=db.backref('users', lazy ='dynamic'))
    ecoes = db.relationship('ECOE', backref='ecoes', lazy='dynamic')

    def __init__(self, nombre=''):
        self.name = nombre

    #def get_organizacion_ids(self):
     #   ids = Organizacion.query.with_entities(Organizacion.id_organizacion).all()
      #  return list(np.squeeze(ids))

    def get_user_organization(self, user_id):

        ids = db.session.query(orguser).filter_by(id_user=user_id)
        organizations=[]

        for id in ids:
            organizations.append(Organization().get_organization(id.id_organization))

        return organizations

    def get_organization(self, id):
        organization = Organization.query.filter_by(id_organization=id).first()
        return organization

    def get_last_organization(self):
        organizations = Organization.query.all()

        numOrg = len(organizations)
        organization = organizations[numOrg - 1]

        return organization

    def post_organization(self):
        db.session.add(self)
        db.session.commit()


    def put_organization(self, nombre):
        self.name = nombre
        db.session.commit()

    def delete_organization(self):
        db.session.delete(self)
        db.session.commit()

    def exist_organization_user(self, id_user):
        for user in self.users:
            if(user.id_user==id_user):
                return True
        return False


    def put_organization_user(self, user):
        self.users.append(user)
        db.session.commit()


    def delete_organization_user(self, user):
        self.users.remove(user)
        db.session.commit()

    def get_user_organizations(self, user_id):

        ids = db.session.query(orguser).filter_by(id_user=user_id)
        organizations=[]

        for id in ids:
            organizations.append(Organization().get_organization(id.id_organization))

        return organizations

    def exist_organization_ecoe(self, id_ecoe):
        for ecoe in self.ecoes:
            if(ecoe.id==id_ecoe):
                return True
        return False

