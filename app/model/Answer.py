from app import db
from app.model.Student import Student
from app.model.Option import Option


class Answer(db.Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    id_option = db.Column(db.Integer, db.ForeignKey(Option.id), nullable=False)
    option = db.relationship(Option, backref='answers')
    id_student = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    student = db.relationship(Student, backref='answers')

    __table_args__ = (
        db.UniqueConstraint(id_option, id_student, name='_option_student_uc'),
    )
