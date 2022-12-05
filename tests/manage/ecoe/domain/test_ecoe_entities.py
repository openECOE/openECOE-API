from datetime import date, datetime, time
import pytest
from modules.manage.ecoe.domain.entities import ECOE, Coordinator
from modules.manage.ecoe.domain.value_objects import Shift, Status, Round
from seedwork.domain.value_objects import UUID



class TestEcoe:
    def test_constructor_should_create_instance(self):
        ecoe = ECOE(id=ECOE.next_id(), name="foo")

        assert isinstance(ecoe, ECOE)
        assert ecoe.name == "foo"

    def test_change_main_attributes(self):
        ecoe = ECOE(id=ECOE.next_id(), name="foo")
        
        ecoe.change_main_attributes(name="foo-change")
        
        assert ecoe.name == "foo-change"

    def test_publish_ecoe(self):
        ecoe = ECOE(id=ECOE.next_id(), name="foo")
        
        ecoe.publish()

        assert ecoe.status == Status.PUBLISHED

    def test_archive_ecoe(self):
        ecoe = ECOE(id=ECOE.next_id(), name="foo")
        
        ecoe.archive()

        assert ecoe.status == Status.ARCHIVED
        
    def test_draft_ecoe(self):
        ecoe = ECOE(id=ECOE.next_id(), name="foo")
        
        ecoe.publish()
        ecoe.draft()

        assert ecoe.status == Status.DRAFT
        
    def test_is_coordinator(self):
        ecoe = ECOE(id=ECOE.next_id(), name="foo")
        
        uuid_1 = UUID.v4()
        coordinator_1 = Coordinator(user_id=uuid_1)
        uuid_2 = UUID.v4()
        coordinator_2 = Coordinator(user_id=uuid_2)
        
        ecoe.add_coordinator(coordinator_1)
        
        assert ecoe.is_coordinator(coordinator=coordinator_1) == True
        assert ecoe.is_coordinator(coordinator=coordinator_2) == False
        
        


class TestCoordinators:        
    def test_add_coordinators(self):
        ecoe = ECOE(id=ECOE.next_id(), name="foo")
        uuid_1 = UUID.v4()
        coordinator_1 = Coordinator(user_id=uuid_1)
        uuid_2 = UUID.v4()
        coordinator_2 = Coordinator(user_id=uuid_2)
        
        ecoe.add_coordinator(coordinator_1)
        assert len(ecoe.coordinators) == 1
        assert ecoe.coordinators[0].user_id == uuid_1
        
        ecoe.add_coordinator(coordinator_2)
        assert len(ecoe.coordinators) == 2
        assert ecoe.coordinators[1].user_id == uuid_2
        
    def test_remove_coordinators(self):
        ecoe = ECOE(id=ECOE.next_id(), name="foo")
        uuid_1 = UUID.v4()
        coordinator_1 = Coordinator(user_id=uuid_1)
        uuid_2 = UUID.v4()
        coordinator_2 = Coordinator(user_id=uuid_2)
        
        ecoe.add_coordinator(coordinator_1)
        ecoe.add_coordinator(coordinator_2)
        assert len(ecoe.coordinators) == 2
        
        ecoe.del_coordinator(coordinator_1)
        
        assert len(ecoe.coordinators) == 1
        assert ecoe.coordinators[0].user_id == uuid_2
        

class TestRounds:
    def test_add_rounds(self):
        ecoe = ECOE(id=ECOE.next_id(), name="foo")
        round_1 = Round(name= "Round 1", code="1")
        round_2 = Round(name= "Round 2", code="2")
        
        ecoe.add_round(round=round_1)
        assert len(ecoe.rounds) == 1
        assert ecoe.rounds[0].name == round_1.name
        
        ecoe.add_round(round=round_2)
        assert len(ecoe.rounds) == 2
        assert ecoe.rounds[1].name == round_2.name
        
    def test_remove_rounds(self):
        ecoe = ECOE(id=ECOE.next_id(), name="foo")
        round_1 = Round(name= "Round 1", code="1")
        round_2 = Round(name= "Round 1", code="2")
        
        ecoe.add_round(round=round_1)
        ecoe.add_round(round=round_2)
        assert len(ecoe.rounds) == 2
        
        ecoe.del_round(round=round_1)
        assert len(ecoe.rounds) == 1
        assert ecoe.rounds[0].name == round_2.name


class TestShifts:
    def test_add_shifts(self):
        ecoe = ECOE(id=ECOE.next_id(), name="foo")
        shift_1 = Shift(code="1", day=date(2022, 11, 1))
        
        shift_1.times.append(time(10,30))
        shift_1.times.append(time(11,30))
        
        shift_2 = Shift(code="2", day=datetime.now())
        
        ecoe.add_shift(shift=shift_1)
        assert len(ecoe.shifts) == 1
        assert ecoe.shifts[0].code == shift_1.code
        
        ecoe.add_shift(shift=shift_2)
        assert len(ecoe.shifts) == 2
        assert ecoe.shifts[1].code == shift_2.code
        
    def test_remove_shift(self):
        ecoe = ECOE(id=ECOE.next_id(), name="foo")
        shift_1 = Shift(code="1", day=date(2022, 11, 1))
        shift_2 = Shift(code="2", day=datetime.now())
        
        ecoe.add_shift(shift=shift_1)
        ecoe.add_shift(shift=shift_2)
        assert len(ecoe.shifts) == 2
        
        ecoe.del_shift(shift=shift_1)
        assert len(ecoe.shifts) == 1
        assert ecoe.shifts[0].code == shift_2.code