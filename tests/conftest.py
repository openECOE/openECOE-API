import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.seedwork.infrastructure.database import Base

from src.config.api_config import ApiConfig


@pytest.fixture
def db_session():
    config = ApiConfig()
    engine = create_engine(config.DATABASE_URL, echo=config.DEBUG)
    with engine.begin() as connection:
        Base.metadata.drop_all(connection)
        Base.metadata.create_all(connection)

    with Session(engine) as session:
        yield session
