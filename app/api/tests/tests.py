import unittest
from app import create_app, db
from app.model import Organization, ECOE, Student, Area, Station, Shift, Round, Planner, Stage, Schedule, Event, QBlock, Question, Option
from app.api import OrganizationResource, EcoeResource, StudentResource, AreaResource, StationResource
from app import api_app
from config import BaseConfig
from datetime import datetime
from flask_potion import Api
from app.api.tests import BaseTestCase
from flask import request, url_for
from flask import Flask
# from flask_testing import TestCase


class UserModelCase(BaseTestCase):
    # def setUp(self):
    #     self.app = create_app(TestConfig)
    #     self.app_context = self.app.app_context()
    #     self.app_context.push()
    #     db.create_all()
    #
    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()
    #     self.app_context.pop()

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

    def test_api_organization(self):
        response = self.client.post('/api/organization', data={'name': 'UMH 1'})

        self.assertEqual({
            "$uri": "/api/organization/1",
            "ecoes": [],
            "name": "UMH 1"
        }, response.json)

        self.assertEqual({
            'id': 1,
            'name': 'UMH 1'
        }, OrganizationResource.manager.read(1))

        response = self.client.patch('/api/organization/1', data={'name': 'UMH 5'})
        self.assertEqual({
            "$uri": "/api/organization/1",
            "ecoes": [],
            "name": "UMH 5"
        }, response.json)

        self.client.post('/api/organization', data={'name': 'UMH 2'})
        self.client.post('/api/organization', data={'name': 'UMH 3'})
        response = self.client.get("/api/organization")

        self.assertEqual([
            {
                "$uri": "/api/organization/1",
                "ecoes": [],
                "name": "UMH 5"
            },
            {
                "$uri": "/api/organization/2",
                "ecoes": [],
                "name": "UMH 2"
            },
            {
                "$uri": "/api/organization/3",
                "ecoes": [],
                "name": "UMH 3"
            }
        ], response.json)

        response = self.client.get('/api/organization?where={"name":"UMH 2"}')
        self.assertEqual([
            {
                "$uri": "/api/organization/2",
                "ecoes": [],
                "name": "UMH 2"
            }
        ], response.json)

        response = self.client.delete('/api/organization/3')
        self.assertStatus(response, 204)

        response = self.client.patch('/api/organization/2', data={'name': None})
        self.assert400(response)

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

    def test_api_ecoe(self):
        self.test_api_organization()
        response = self.client.post('/api/ecoe', data={'name': 'ECOE 1', 'organization': 1})

        self.assertEqual({
            "$uri": "/api/ecoe/1",
            "areas": [],
            "name": "ECOE 1",
            "organization": {
                "$ref": "/api/organization/1"
            },
            "rounds": [],
            "schedules": [],
            "shifts": [],
            "stations": [],
            "students": []
        }, response.json)

        self.assertEqual({
            "$uri": "/api/ecoe/1",
            "areas": [],
            "name": "ECOE 1",
            "organization": {
                "$ref": "/api/organization/1"
            },
            "rounds": [],
            "schedules": [],
            "shifts": [],
            "stations": [],
            "students": []
        }, EcoeResource.manager.read(1))

        response = self.client.patch('/api/ecoe/1', data={'name': 'ECOE TEST 1'})
        self.assertEqual({
            "$uri": "/api/ecoe/1",
            "areas": [],
            "name": "ECOE TEST 1",
            "organization": {
                "$ref": "/api/organization/1"
            },
            "rounds": [],
            "schedules": [],
            "shifts": [],
            "stations": [],
            "students": []
        }, response.json)

        self.client.post('/api/ecoe', data={'name': 'ECOE 2', 'organization': 1})
        self.client.post('/api/ecoe', data={'name': 'ECOE 3', 'organization': 2})
        response = self.client.get("/api/ecoe")

        self.assertEqual([
            {
                "$uri": "/api/ecoe/1",
                "areas": [],
                "name": "ECOE TEST 1",
                "organization": {
                    "$ref": "/api/organization/1"
                },
                "rounds": [],
                "schedules": [],
                "shifts": [],
                "stations": [],
                "students": []
            },
            {
                "$uri": "/api/ecoe/2",
                "areas": [],
                "name": "ECOE 2",
                "organization": {
                    "$ref": "/api/organization/1"
                },
                "rounds": [],
                "schedules": [],
                "shifts": [],
                "stations": [],
                "students": []
            },
            {
                "$uri": "/api/ecoe/3",
                "areas": [],
                "name": "ECOE 3",
                "organization": {
                    "$ref": "/api/organization/2"
                },
                "rounds": [],
                "schedules": [],
                "shifts": [],
                "stations": [],
                "students": []
            }
        ], response.json)

        response = self.client.get('/api/ecoe?where={"name":"ECOE 2"}')
        self.assertEqual([
            {
                "$uri": "/api/ecoe/2",
                "areas": [],
                "name": "ECOE 2",
                "organization": {
                    "$ref": "/api/organization/1"
                },
                "rounds": [],
                "schedules": [],
                "shifts": [],
                "stations": [],
                "students": []
            }
        ], response.json)

        response = self.client.delete('/api/ecoe/3')
        self.assertStatus(response, 204)

        response = self.client.patch('/api/ecoe/2', data={'name': None})
        self.assert400(response)

        response = self.client.get('/api/organization/1')
        self.assertEqual({
            "$uri": "/api/organization/1",
            "ecoes": [
                {
                    "$uri": "/api/ecoe/1",
                    "areas": [],
                    "name": "ECOE TEST 1",
                    "organization": {
                        "$ref": "/api/organization/1"
                    },
                    "rounds": [],
                    "schedules": [],
                    "shifts": [],
                    "stations": [],
                    "students": []
                },
                {
                    "$uri": "/api/ecoe/2",
                    "areas": [],
                    "name": "ECOE 2",
                    "organization": {
                        "$ref": "/api/organization/1"
                    },
                    "rounds": [],
                    "schedules": [],
                    "shifts": [],
                    "stations": [],
                    "students": []
                }
            ],
            "name": "UMH 5"
        }, response.json)

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

    def test_api_students(self):
        self.test_api_ecoe()
        response = self.client.post('/api/student', data={'name': 'Student 1', 'surnames': 'Student 1 surnames', 'ecoe': 1, 'dni': '123456789'})

        self.assertEqual({
            "$uri": "/api/student/1",
            "answers": [],
            "dni": "123456789",
            "ecoe": {
                "$ref": "/api/ecoe/1"
            },
            "name": "Student 1",
            # TODO: revisar estos None
            "planner": None,
            "planner_order": None,
            "surnames": "Student 1 surnames"
        }, response.json)

        self.assertEqual({
            "$uri": "/api/student/1",
            "answers": [],
            "dni": "123456789",
            "ecoe": {
                "$ref": "/api/ecoe/1"
            },
            "name": "Student 1",
            # TODO: revisar estos None
            "planner": None,
            "planner_order": None,
            "surnames": "Student 1 surnames"
        }, StudentResource.manager.read(1))

        response = self.client.patch('/api/student/1', data={'name': 'Student Test 1'})
        self.assertEqual({
            "$uri": "/api/student/1",
            "answers": [],
            "dni": "123456789",
            "ecoe": {
                "$ref": "/api/ecoe/1"
            },
            "name": "Student Test 1",
            # TODO: revisar estos None
            "planner": None,
            "planner_order": None,
            "surnames": "Student 1 surnames"
        }, response.json)

        self.client.post('/api/student', data={'name': 'Student 2', 'surnames': 'Student 2 surnames', 'ecoe': 1, 'dni': '223456789'})
        self.client.post('/api/student', data={'name': 'Student 3', 'surnames': 'Student 3 surnames', 'ecoe': 1, 'dni': '323456789'})
        response = self.client.get("/api/student")

        self.assertEqual([
            {
                "$uri": "/api/student/1",
                "answers": [],
                "dni": "123456789",
                "ecoe": {
                    "$ref": "/api/ecoe/1"
                },
                "name": "Student Test 1",
                # TODO: revisar estos None
                "planner": None,
                "planner_order": None,
                "surnames": "Student 1 surnames"
            },
            {
                "$uri": "/api/student/2",
                "answers": [],
                "dni": "223456789",
                "ecoe": {
                    "$ref": "/api/ecoe/1"
                },
                "name": "Student 2",
                # TODO: revisar estos None
                "planner": None,
                "planner_order": None,
                "surnames": "Student 2 surnames"
            },
            {
                "$uri": "/api/student/3",
                "answers": [],
                "dni": "323456789",
                "ecoe": {
                    "$ref": "/api/ecoe/1"
                },
                "name": "Student 3",
                # TODO: revisar estos None
                "planner": None,
                "planner_order": None,
                "surnames": "Student 3 surnames"
            }
        ], response.json)

        response = self.client.get('/api/student?where={"name":"Student 2"}')
        self.assertEqual([
            {
                "$uri": "/api/student/2",
                "answers": [],
                "dni": "223456789",
                "ecoe": {
                    "$ref": "/api/ecoe/1"
                },
                "name": "Student 2",
                # TODO: revisar estos None
                "planner": None,
                "planner_order": None,
                "surnames": "Student 2 surnames"
            }
        ], response.json)

        response = self.client.delete('/api/student/3')
        self.assertStatus(response, 204)

        response = self.client.patch('/api/student/2', data={'name': None})
        self.assert400(response)

        response = self.client.get('/api/ecoe/1')
        self.assertEqual({
            "$uri": "/api/ecoe/1",
            "areas": [],
            "name": "ECOE TEST 1",
            "organization": {
                "$ref": "/api/organization/1"
            },
            "rounds": [],
            "schedules": [],
            "shifts": [],
            "stations": [],
            "students": [
                {
                    "$ref": "/api/student/1"
                },
                {
                    "$ref": "/api/student/2"
                }
            ]
        }, response.json)

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

    def test_stations(self):
        self.test_ecoe()
        ecoe = ECOE.query.first()
        station1 = Station(id=1, name='Station 1', id_ecoe=ecoe.id, order=1)
        station2 = Station(id=2, name='Station 2', id_ecoe=ecoe.id, order=2)
        station3 = Station(id=3, name='Station 3', id_ecoe=ecoe.id, order=3)
        station4 = Station(name='Station 4', id_ecoe=ecoe.id, order=4)

        db.session.add(station1)
        db.session.add(station2)
        db.session.add(station3)
        db.session.add(station4)
        db.session.commit()

        self.assertIn(station1, ecoe.stations)
        self.assertIn(station2, ecoe.stations)

        db.session.delete(station4)
        db.session.commit()
        station4 = Station.query.filter(Station.id == station4.id).first()
        self.assertIsNone(station4)

        self.assertEqual(station3.name, 'Station 3')
        self.assertEqual(station3.id_ecoe, 1)

        station3.name = 'Sta 3'
        db.session.commit()
        self.assertEqual(station3.name, 'Sta 3')

    def test_shift(self):
        self.test_ecoe()
        ecoe = ECOE.query.first()
        shift1 = Shift(id=1, shift_code='Shift 1', time_start=datetime(2018, 5, 23, 9, 0, 0), id_ecoe=ecoe.id)
        shift2 = Shift(id=2, shift_code='Shift 2', time_start=datetime(2018, 5, 23, 10, 0, 0), id_ecoe=ecoe.id)
        shift3 = Shift(id=3, shift_code='Shift 3', time_start=datetime(2018, 5, 23, 11, 0, 0), id_ecoe=ecoe.id)
        shift4 = Shift(shift_code='Shift 4', time_start=datetime(2018, 5, 23, 12, 0, 0), id_ecoe=ecoe.id)

        db.session.add(shift1)
        db.session.add(shift2)
        db.session.add(shift3)
        db.session.add(shift4)
        db.session.commit()

        self.assertIn(shift1, ecoe.shifts)
        self.assertIn(shift2, ecoe.shifts)
        self.assertIn(shift3, ecoe.shifts)

        db.session.delete(shift4)
        db.session.commit()
        shift4 = Shift.query.filter(Shift.id == shift4.id).first()
        self.assertIsNone(shift4)

        self.assertEqual(shift3.shift_code, 'Shift 3')
        self.assertEqual(shift3.id_ecoe, 1)

        shift3.shift_code = 'Shift code 3'
        db.session.commit()
        self.assertEqual(shift3.shift_code, 'Shift code 3')

    # def test_rounds(self):
    #     self.test_ecoe()
    #     ecoe = ECOE.query.first()
    #     round1 = Round(id=1, description='Description round 1', round_code='Round A', id_ecoe=ecoe.id)
    #     round2 = Round(id=2, description='Description round 2', round_code='Round B', id_ecoe=ecoe.id)
    #     round3 = Round(description='Description round 3', round_code='Round C', id_ecoe=ecoe.id)
    #
    #     db.session.add(round1)
    #     db.session.add(round2)
    #     db.session.add(round3)
    #     db.session.commit()
    #
    #     self.assertIn(round1, ecoe.rounds)
    #     self.assertIn(round2, ecoe.rounds)
    #     self.assertIn(round3, ecoe.rounds)
    #
    #     db.session.delete(shift4)
    #     db.session.commit()
    #     shift4 = Shift.query.filter(Shift.id == shift4.id).first()
    #     self.assertIsNone(shift4)
    #
    #     self.assertEqual(shift3.shift_code, 'Shift 3')
    #     self.assertEqual(shift3.id_ecoe, 1)
    #
    #     shift3.shift_code = 'Shift code 3'
    #     db.session.commit()
    #     self.assertEqual(shift3.shift_code, 'Shift code 3')

    # def test(self):
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

