import unittest
from app import create_app, db
from app.model import Organization, ECOE, Student, Area, Station, Shift, Round, Planner, Stage, Schedule, Event, QBlock, Question, Option
from config import BaseConfig
from flask import request


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 4
    DEBUG = True
    API_AUTH = True


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_organization(self):
        organization = Organization(id=1, name='Orga 1')
        db.session.add(organization)
        db.session.commit()

        self.assertEqual(organization.name, 'Orga 1')

        organization.name = 'Organization 1'
        self.assertEqual(organization.name, 'Organization 1')

        db.session.delete(organization)
        db.session.commit()
        organization = Organization.query.filter(Organization.id == organization.id).first()
        self.assertIsNone(organization)

        organization = Organization(id=1, name='Orga 1')
        db.session.add(organization)
        db.session.commit()

    def test_ecoe(self):
        self.test_organization()
        organization = Organization.query.first()
        ecoe1 = ECOE(id=1, name='Ecoe1', id_organization=organization.id)
        ecoe2 = ECOE(id=2, name='Ecoe2', id_organization=organization.id)

        db.session.add(ecoe1)
        db.session.add(ecoe2)
        db.session.commit()

        self.assertIn(ecoe1, organization.ecoes)
        self.assertIn(ecoe2, organization.ecoes)

        db.session.delete(ecoe2)
        db.session.commit()
        ecoe2 = ECOE.query.filter(ECOE.id == ecoe2.id).first()
        self.assertIsNone(ecoe2)

        self.assertEqual(ecoe1.name, 'Ecoe1')
        self.assertEqual(ecoe1.id_organization, 1)

        ecoe1.name = 'ECOE 1'
        db.session.commit()
        self.assertEqual(ecoe1.name, 'ECOE 1')

    def test_students(self):
        self.test_ecoe()
        ecoe = ECOE.query.first()
        student1 = Student(id=1, name='St1', surnames='St1 surname', id_ecoe=ecoe.id, dni='12345678')
        student2 = Student(id=2, name='St2', surnames='St2 surname', id_ecoe=ecoe.id, dni='13345678')
        student3 = Student(id=3, name='St3', surnames='St3 surname', id_ecoe=ecoe.id, dni='14345678')
        student4 = Student(name='St4', surnames='St4 surname', id_ecoe=ecoe.id, dni='15345678')

        db.session.add(student1)
        db.session.add(student2)
        db.session.add(student3)
        db.session.add(student4)
        db.session.commit()

        self.assertIn(student1, ecoe.students)
        self.assertIn(student2, ecoe.students)

        db.session.delete(student4)
        db.session.commit()
        student4 = Student.query.filter(Student.id == student4.id).first()
        self.assertIsNone(student4)

        self.assertEqual(student3.dni, '14345678')
        self.assertEqual(student3.id_ecoe, 1)

        student3.surnames = 'Student3 surname'
        db.session.commit()
        self.assertEqual(student3.surnames, 'Student3 surname')

    def test_areas(self):
        self.test_ecoe()
        ecoe = ECOE.query.first()
        area1 = Area(id=1, name='Area 1', id_ecoe=ecoe.id)
        area2 = Area(id=2, name='Area 2', id_ecoe=ecoe.id)
        area3 = Area(id=3, name='Area 3', id_ecoe=ecoe.id)
        area4 = Area(name='Area 4', id_ecoe=ecoe.id)

        db.session.add(area1)
        db.session.add(area2)
        db.session.add(area3)
        db.session.add(area4)
        db.session.commit()

        self.assertIn(area1, ecoe.areas)
        self.assertIn(area2, ecoe.areas)

        db.session.delete(area4)
        db.session.commit()
        area4 = Area.query.filter(Area.id == area4.id).first()
        self.assertIsNone(area4)

        self.assertEqual(area3.name, 'Area 3')
        self.assertEqual(area3.id_ecoe, 1)

        area3.name = 'Anamnesis'
        db.session.commit()
        self.assertEqual(area3.name, 'Anamnesis')

    # def test(self):
    #     area1 = Area(name='Area 1', id_ecoe=ecoe1.id)
    #     area2 = Area(name='Area 2', id_ecoe=ecoe1.id)
    #     area3 = Area(name='Area 3', id_ecoe=ecoe1.id)
    #     area4 = Area(name='Area 4', id_ecoe=ecoe2.id)
    #
    #     station1 = Station(name='Station 1', id_ecoe=ecoe1.id, order=1)
    #     station2 = Station(name='Station 2', id_ecoe=ecoe1.id, order=2)
    #     station3 = Station(name='Station 3', id_ecoe=ecoe1.id, order=3)
    #     station4 = Station(name='Station 4', id_ecoe=ecoe2.id, order=1)
    #     station5 = Station(name='Station 5', id_ecoe=ecoe2.id, order=3)
    #
    #     shift1 = Shift(shift_code='Shift 1', time_start='2018-05-23T09:00:00+02:00', id_ecoe=ecoe1.id)
    #     shift2 = Shift(shift_code='Shift 2', time_start='2018-05-23T10:00:00+02:00', id_ecoe=ecoe1.id)
    #     shift3 = Shift(shift_code='Shift 3', time_start='2018-05-23T11:00:00+02:00', id_ecoe=ecoe1.id)
    #     shift4 = Shift(shift_code='Shift 4', time_start='2018-05-23T12:00:00+02:00', id_ecoe=ecoe1.id)
    #     shift5 = Shift(shift_code='Shift 5', time_start='2018-05-24T09:00:00+02:00', id_ecoe=ecoe1.id)
    #     shift6 = Shift(shift_code='Shift 6', time_start='2018-05-23T09:00:00+02:00', id_ecoe=ecoe2.id)
    #     shift7 = Shift(shift_code='Shift 7', time_start='2018-05-23T13:00:00+02:00', id_ecoe=ecoe2.id)
    #
    #     round1 = Round(description='Description round 1', round_code='Round A', id_ecoe=ecoe1.id)
    #     round2 = Round(description='Description round 2', round_code='Round B', id_ecoe=ecoe1.id)
    #     round3 = Round(description='Description round 3', round_code='Round C', id_ecoe=ecoe1.id)
    #     round4 = Round(description='Description round 1', round_code='Round A', id_ecoe=ecoe2.id)
    #
    #     planner1 = Planner(id_shift=shift1.id, id_round=round1.id)
    #     planner2 = Planner(id_shift=shift2.id, id_round=round1.id)
    #     planner3 = Planner(id_shift=shift3.id, id_round=round1.id)
    #     planner4 = Planner(id_shift=shift4.id, id_round=round1.id)
    #     planner5 = Planner(id_shift=shift5.id, id_round=round2.id)
    #     planner6 = Planner(id_shift=shift7.id, id_round=round4.id)
    #
    #     stage1 = Stage(duration=540, order=0, name='Evaluation')
    #     stage2 = Stage(duration=120, order=1, name='Rest')
    #
    #     schedule1 = Schedule(id_stage=stage2.id, id_ecoe=ecoe1.id)
    #
    #     event1 = Event(id_schedule=schedule1.id, time=0, sound='start.mp3', text='Station starts')
    #     event1 = Event(id_schedule=schedule1.id, time=360, sound='6min.mp3')
    #     event1 = Event(id_schedule=schedule1.id, time=540, sound='finish.mp3', text='Leave station')
    #
    #     student1.planner_order = planner1.id
    #     student2.planner_order = planner1.id
    #     student3.planner_order = planner1.id
    #     student4.planner_order = planner1.id
    #
    #     qblock1 = QBlock(name='Qblock 1', id_station=station1.id, order=0)
    #     qblock2 = QBlock(name='Qblock 2', id_station=station1.id, order=1)
    #     qblock3 = QBlock(name='Qblock 3', id_station=station1.id, order=2)
    #     qblock4 = QBlock(name='Qblock 4', id_station=station2.id, order=0)
    #     qblock5 = QBlock(name='Qblock 5', id_station=station3.id, order=0)
    #     qblock6 = QBlock(name='Qblock 6', id_station=station4.id, order=0)
    #
    #     question1 = Question(reference='Ref 1', description='Question 1', id_area=area1.id, question_type='RB')
    #     question2 = Question(reference='Ref 2', description='Question 2', id_area=area1.id, question_type='CH')
    #     question3 = Question(reference='Ref 3', description='Question 3', id_area=area1.id, question_type='RB')
    #     question4 = Question(reference='Ref 4', description='Question 4', id_area=area2.id, question_type='CH')
    #     question5 = Question(reference='Ref 5', description='Question 5', id_area=area2.id, question_type='RB')
    #     question6 = Question(reference='Ref 6', description='Question 6', id_area=area2.id, question_type='CH')
    #     question7 = Question(reference='Ref 6', description='Question 6', id_area=area2.id, question_type='RB')
    #
    #     qblock1.questions = 1
    #     qblock1.questions = 2
    #     qblock1.questions = 3
    #     qblock1.questions = 4
    #     qblock2.questions = 5
    #     qblock2.questions = 6
    #     qblock2.questions = 7
    #
    #     option1 = Option(points=0, id_question=question1.id, label='No', order=1)
    #     option2 = Option(points=10, id_question=question1.id, label='Si', order=2)
    #     option3 = Option(points=10, id_question=question2.id, label='España', order=1)
    #     option4 = Option(points=0, id_question=question2.id, label='Francia', order=2)
    #     option5 = Option(points=10, id_question=question2.id, label='Portugal', order=3)
    #     option6 = Option(points=0, id_question=question2.id, label='Italia', order=4)
    #
    #     student1.answers = option1.id
    #     student1.answers = option3.id
    #     student1.answers = option5.id
    #     student2.answers = option2.id
    #     student2.answers = option4.id

        # db.session.add_all([p1, p2, p3, p4])
        # db.session.commit()

    # def test_password_hashing(self):
    #     u = User(username='susan')
    #     u.set_password('cat')
    #     self.assertFalse(u.check_password('dog'))
    #     self.assertTrue(u.check_password('cat'))

