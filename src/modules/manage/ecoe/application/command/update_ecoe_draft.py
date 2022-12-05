from seedwork.application.commands import Command
from seedwork.application.command_handlers import CommandResult
from seedwork.application.decorators import command_handler
from seedwork.domain.value_objects import UUID
from modules.manage.ecoe.domain.entities import ECOE
from modules.manage.ecoe.domain.repositories import EcoeRepository


class UpdateEcoeDraftCommand(Command):
    """A command for updating a ecoe"""

    ecoe_id: UUID
    name: str
    # modify_user_id: UUID


@command_handler
def update_ecoe_draft(
    command: UpdateEcoeDraftCommand, repository: EcoeRepository
) -> CommandResult:
    ecoe: ECOE = repository.get_by_id(command.ecoe_id)
    events = ecoe.change_main_attributes(
        name=command.name)
    repository.update(ecoe)
    return CommandResult.ok(result=ecoe, events=events)
