from app import db
from app.model.many_to_many_tables import students_options


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surnames = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(10))  # dni is not unique

    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'), nullable=False)
    id_planner = db.Column(db.Integer, db.ForeignKey('planner.id'), nullable=True)
    planner_order = db.Column(db.Integer)

    answers = db.relationship('Option', secondary=students_options, lazy=True, back_populates='students')

    __table_args__ = (
        db.UniqueConstraint(name, surnames, id_ecoe, name='student_name_ecoe_uk'),
    )
