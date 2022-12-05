from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from modules.manage.ecoe.domain.value_objects import Coordinator, Status


class CurrentUser(BaseModel):
    id: UUID
    username: str

    @classmethod
    def fake_user(cls):
        return CurrentUser(id=uuid4(), username="fake_user")


class EcoeWriteModel(BaseModel):
    name: str


class EcoeReadModel(BaseModel):
    id: UUID
    name: str = "ECOE UMH"
    status: str = Status.DRAFT
    coordinators: List[Coordinator] = Field(default_factory=list)


class EcoeIndexModel(BaseModel):
    data: List[EcoeReadModel]
