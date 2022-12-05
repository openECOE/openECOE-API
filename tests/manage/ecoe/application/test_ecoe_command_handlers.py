from modules.manage.ecoe.application.command.add_ecoe_coordinator import AddEcoeCoordinatorCommand, add_ecoe_coordinator
from modules.manage.ecoe.application.command.archive_ecoe import (
    ArchiveEcoeCommand,
    archive_ecoe_draft
)
from modules.manage.ecoe.application.command.create_ecoe_draft import (
    CreateEcoeDraftCommand,
    create_ecoe_draft
)
from modules.manage.ecoe.application.command.publish_ecoe import (
    PublishEcoeDraftCommand,
    publish_ecoe_draft
)
from modules.manage.ecoe.application.command.update_ecoe_draft import (
    UpdateEcoeDraftCommand,
    update_ecoe_draft
)
from modules.manage.ecoe.domain.entities import ECOE
from modules.manage.ecoe.domain.value_objects import Status
from seedwork.domain.value_objects import UUID

from seedwork.infrastructure.repository import InMemoryRepository


def test_create_ecoe_draft():

    # arrange
    command = CreateEcoeDraftCommand(
        name="foo"
    )
    repository = InMemoryRepository()

    # act
    result = create_ecoe_draft(command, repository)
    
    # assert
    assert repository.get_by_id(result.result.id).name == "foo"
    assert result.has_errors() is False
    

def test_update_ecoe_draft():
    # arrange
    repository = InMemoryRepository()
    ecoe = ECOE(id=ECOE.next_id(), name="foo")
    repository.insert(ecoe)
    
    command = UpdateEcoeDraftCommand(
        ecoe_id=ecoe.id,
        modify_user_id= UUID.v4(),
        name="foo2"
    )

    # act
    result = update_ecoe_draft(command, repository)
    
    # assert
    assert repository.get_by_id(result.result.id).name == "foo2"
    assert result.is_ok()
    

def test_publish_ecoe():
    # arrange
    ecoe_repository = InMemoryRepository()
    ecoe = ECOE(id=ECOE.next_id(), name="foo")
    ecoe_repository.insert(ecoe)

    command = PublishEcoeDraftCommand(
        ecoe_id=ecoe.id,
        modify_user_id=UUID.v4()
    )

    # act
    result = publish_ecoe_draft(
        command, repository=ecoe_repository
    )

    # assert
    assert result.is_ok()
    assert ecoe.status == Status.PUBLISHED
    

def test_archive_ecoe():
    
    # arrange
    ecoe_repository = InMemoryRepository()
    ecoe = ECOE(id=ECOE.next_id(), name="foo")
    ecoe_repository.insert(ecoe)

    command = ArchiveEcoeCommand(
        ecoe_id=ecoe.id,
        modify_user_id=UUID.v4()
    )

    # act
    result = archive_ecoe_draft(
        command, repository=ecoe_repository
    )

    # assert
    assert result.is_ok()
    assert ecoe.status == Status.ARCHIVED
    
    
def test_add_coordinator():
    
    ecoe_repository = InMemoryRepository()
    ecoe = ECOE(id=ECOE.next_id(), name="foo")
    ecoe_repository.insert(ecoe)
    
    test_user_id = UUID.v4()
    
    command = AddEcoeCoordinatorCommand(
        ecoe_id=ecoe.id,
        user_id=test_user_id
    )
    
    result = add_ecoe_coordinator(
        command, ecoe_repository
    )
    
    assert result.is_ok()
    assert len(ecoe.coordinators) == 1