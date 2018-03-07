from ws import db

class Student(db.Model):
    __tablename__="stu"

    id_student = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    dni = db.Column(db.String(25))
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'))
    id_round = db.Column(db.Integer, db.ForeignKey('round.id_round'))

    def __init__(self, nombre='', dni='', id_ecoe=0):
        self.name = nombre
        self.dni = dni
        self.id_ecoe = id_ecoe

    def get_student(self, id):
        student = Student.query.filter_by(id_student=id).first()
        return student

    def post_student(self):
        db.session.add(self)
        db.session.commit()

    def put_student(self, name, dni, id_ecoe):
        self.dni = dni
        self.name = name
        self.id_ecoe = id_ecoe
        db.session.commit()

    def put_student_id_round(self, id_round):
        self.id_round = id_round

        db.session.commit()

    def delete_student(self):
        db.session.delete(self)
        db.session.commit()

    def delete_student_id_round(self):
        self.id_round = None
        db.session.commit()

    def get_last_student(self):
        students = Student.query.all()

        numStudent = len(students)
        student = students[numStudent-1]

        return student
