from app import db

qblocks_questions = db.Table('qblocks_questions',
    db.Column('qblock_id', db.Integer, db.ForeignKey('qblock.id'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True)
)

students_options = db.Table('students_options',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('option_id', db.Integer, db.ForeignKey('option.id'), primary_key=True)
)