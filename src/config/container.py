import uuid
import logging
from sqlalchemy import create_engine
from dependency_injector import containers, providers
from dependency_injector.wiring import inject  # noqa

from modules.iam.module import IdentityAndAccessModule
from modules.iam.application.services import AuthenticationService
from modules.iam.infrastructure.user_repository import PostgresJsonUserRepository
from modules.manage.ecoe.infrastructure.ecoe_repository import PostgresJsonEcoeRepository
from modules.manage.ecoe.module import ManageModule

from seedwork.infrastructure.request_context import RequestContext


def _default(val):
    import uuid

    if isinstance(val, uuid.UUID):
        return str(val)
    raise TypeError()


def dumps(d):
    import json

    return json.dumps(d, default=_default)


class DummyService:
    def __init__(self, config) -> None:
        self.config = config

    def serve(self):
        return f"serving with config {self.config}"


def create_request_context(engine):
    from seedwork.infrastructure.request_context import request_context

    request_context.setup(engine)
    return request_context


def create_engine_once(config):
    engine = create_engine(
        config["DATABASE_URL"], echo=config["DEBUG"], json_serializer=dumps
    )
    from seedwork.infrastructure.database import Base

    # TODO: it seems like a hack, but it works...
    Base.metadata.bind = engine
    return engine


class Container(containers.DeclarativeContainer):
    """Dependency Injection Container

    see https://github.com/ets-labs/python-dependency-injector for more details
    """

    __self__ = providers.Self()

    config = providers.Configuration()
    engine = providers.Singleton(create_engine_once, config)
    dummy_service = providers.Factory(DummyService, config)
    dummy_singleton = providers.Singleton(DummyService, config)

    request_context: RequestContext = providers.Factory(
        create_request_context, engine=engine
    )

    correlation_id = providers.Factory(
        lambda request_context: request_context.correlation_id.get(), request_context
    )

    # iam module and it's dependencies
    user_repository = providers.Factory(
        PostgresJsonUserRepository, db_session=request_context.provided.db_session
    )
    authentication_service = providers.Factory(
        AuthenticationService, user_repository=user_repository
    )
    iam_module = providers.Factory(
        IdentityAndAccessModule, authentication_service=authentication_service
    )
    
    # manage modiule and it's dependencies
    ecoe_repository = providers.Factory(
        PostgresJsonEcoeRepository, db_session=request_context.provided.db_session
    )
    manage_module = providers.Factory(
        ManageModule, ecoe_repository=ecoe_repository
    )
