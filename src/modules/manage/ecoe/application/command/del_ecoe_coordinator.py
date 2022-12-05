from modules.manage.ecoe.domain.entities import ECOE
from modules.manage.ecoe.domain.repositories import EcoeRepository
from seedwork.application.command_handlers import CommandResult
from seedwork.application.commands import Command
from seedwork.application.decorators import command_handler
from seedwork.domain.value_objects import UUID


class RemoveEcoeCoordinatorCommand(Command):
    """A command for remove a Coordinator to ECOE"""

    ecoe_id: UUID
    user_id: UUID


@command_handler
def remove_ecoe_coordinator(
    command: RemoveEcoeCoordinatorCommand, repository: EcoeRepository
) -> CommandResult:
    ecoe: ECOE = repository.get_by_id(command.ecoe_id)
    events = ecoe.del_coordinator(coordinator=command.user_id)
    return CommandResult.ok(result=ecoe, events=events)