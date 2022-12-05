from fastapi import APIRouter, Depends
from modules.manage.ecoe.application.command.add_ecoe_coordinator import AddEcoeCoordinatorCommand
from modules.manage.ecoe.application.command.archive_ecoe import ArchiveEcoeCommand
from modules.manage.ecoe.application.command.publish_ecoe import PublishEcoeDraftCommand
from modules.manage.ecoe.application.command.update_ecoe_draft import UpdateEcoeDraftCommand
from seedwork.infrastructure.request_context import RequestContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from modules.manage.ecoe.module import ManageModule
from modules.manage.ecoe.application.command.create_ecoe_draft import CreateEcoeDraftCommand
from modules.manage.ecoe.application.query.get_ecoe_details import GetEcoeDetails
from modules.manage.ecoe.application.query.get_all_ecoes import GetAllEcoes

from modules.manage.ecoe.application.exceptions import (
    EcoeNotFoundException
)

from config.container import Container, inject
from api.models import EcoeIndexModel, EcoeReadModel, EcoeWriteModel
from api.shared import dependency


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


@router.get("/ecoes", tags=["ecoe"], response_model=EcoeIndexModel)
@inject
async def get_all_ecoes(
    module: ManageModule = dependency(Container.manage_module),
):
    """
    Shows all published ecoes in the catalog
    """
    query = GetAllEcoes()
    query_result = module.execute_query(query)
    return dict(data=query_result.result)


@router.get("/ecoes/{ecoe_id}", tags=["ecoe"], response_model=EcoeReadModel)
@inject
async def get_ecoe_details(
    ecoe_id, module: ManageModule = dependency(Container.manage_module)
):
    """
    Shows ecoe details
    """
    query = GetEcoeDetails(ecoe_id=ecoe_id)
    query_result = module.execute_query(query)
    return query_result.result


@router.post(
    "/ecoes", tags=["ecoe"], status_code=201, response_model=EcoeReadModel
)
@inject
async def create_ecoe(
    request_body: EcoeWriteModel,
    module: ManageModule = dependency(Container.manage_module),
):
    """
    Creates a new ecoe.
    """
    command_result = module.execute_command(
        CreateEcoeDraftCommand(
            name=request_body.name,
        )
    )

    return command_result.result

@router.put(
    "/ecoes/{ecoe_id}", tags=["ecoe"], status_code=201, response_model=EcoeReadModel
)
@inject
async def update_ecoe(
    ecoe_id,
    request_body: EcoeWriteModel,
    module: ManageModule = dependency(Container.manage_module),
    # token: str = Depends(oauth2_scheme)
):
    """
    Update a ecoe.
    """
    command_result = module.execute_command(
        UpdateEcoeDraftCommand(
            ecoe_id=ecoe_id,
            name=request_body.name,
        )
    )

    return command_result.result

@router.post(
    "/ecoes/{ecoe_id}/publish", tags=["ecoe"], status_code=200, response_model=EcoeReadModel
)
@inject
async def publish_ecoe(
    ecoe_id,
    module: ManageModule = dependency(Container.manage_module),
    token: str = Depends(oauth2_scheme)
):
    """
    Publish a ecoe.
    """
    command_result = module.execute_command(
        PublishEcoeDraftCommand(
            ecoe_id=ecoe_id,
            # modify_user_id= "00000"
        )
    )

    return command_result.result

@router.post(
    "/ecoes/{ecoe_id}/archive", tags=["ecoe"], status_code=200, response_model=EcoeReadModel
)
@inject
async def archive_ecoe(
    ecoe_id,
    module: ManageModule = dependency(Container.manage_module),
    # token: str = Depends(oauth2_scheme)
):
    """
    Archive a ecoe.
    """
    command_result = module.execute_command(
        ArchiveEcoeCommand(
            ecoe_id=ecoe_id,
            # modify_user_id= "00000"
        )
    )

    return command_result.result

@router.post(
    "/ecoes/{ecoe_id}/coordinator", tags=["ecoe"], status_code=200, response_model=EcoeReadModel
)
@inject
async def add_ecoe_coordinator(
    ecoe_id,
    user_id,
    module: ManageModule = dependency(Container.manage_module),
    # token: str = Depends(oauth2_scheme)
):
    """
    Add coordinator to ecoe.
    """
    command_result = module.execute_command(
        AddEcoeCoordinatorCommand(
            ecoe_id=ecoe_id,
            user_id=user_id
        )
    )

    return command_result.result