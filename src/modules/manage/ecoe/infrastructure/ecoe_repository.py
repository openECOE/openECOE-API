from contextvars import ContextVar
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import Session
from sqlalchemy_json import mutable_json_type
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

from seedwork.infrastructure.database import Base
from seedwork.infrastructure.json_data_mapper import JSONDataMapper

from modules.manage.ecoe.domain.repositories import EcoeRepository
from modules.manage.ecoe.domain.entities import ECOE


class EcoeModel(Base):
    __tablename__ = "ecoe"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data = Column(mutable_json_type(dbtype=JSONB, nested=True))


class PostgresJsonEcoeRepository(EcoeRepository):
    """ECOE repository implementation"""

    model = EcoeModel

    def __init__(self, db_session: ContextVar, mapper=JSONDataMapper()):
        self._session_cv = db_session.get()
        self.mapper = mapper

    @property
    def session(self) -> Session:
        return self._session_cv

    def get_by_id(self, listing_id: UUID) -> ECOE:
        data = self.session.query(self.model).filter_by(id=str(listing_id)).one()
        entity = self.mapper.data_to_entity(data, ECOE)
        return entity

    def insert(self, entity: ECOE):
        data = self.mapper.entity_to_data(entity, self.model)
        self.session.add(data)

    def update(self, entity: ECOE):
        _ecoe = self.session.query(self.model).filter_by(id=entity.id).one()
        data = self.mapper.entity_to_data(entity, self.model).data
        _ecoe.data = data

    def delete(self, entity: ECOE):
        raise NotImplementedError()

    def count(self) -> int:
        return self.session.query(self.model).count()
