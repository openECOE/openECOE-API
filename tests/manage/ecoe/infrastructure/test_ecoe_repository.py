import pytest
from modules.manage.ecoe.domain.entities import ECOE
from modules.manage.ecoe.infrastructure.ecoe_repository import (
    PostgresJsonEcoeRepository,
)

@pytest.mark.skip
def test_ecoe_repo_is_empty(db_session):
    repo = PostgresJsonEcoeRepository(db_session=db_session)
    assert repo.count() == 0

@pytest.mark.skip
def test_ecoe_persistence(db_session):
    original = ECOE(id=ECOE.next_id(), name="foo")
    repository = PostgresJsonEcoeRepository(db_session=db_session)

    repository.insert(original)
    db_session.commit()

    persisted = repository.get_by_id(original.id)

    assert original == persisted
