from modules.manage.ecoe.domain.entities import ECOE
from modules.manage.ecoe.domain.repositories import EcoeRepository
from modules.manage.ecoe.domain.value_objects import Coordinator
from seedwork.application.command_handlers import CommandResult
from seedwork.application.commands import Command
from seedwork.application.decorators import command_handler
from seedwork.domain.value_objects import UUID


class AddEcoeCoordinatorCommand(Command):
    """A command for add a Coordinator to ECOE"""

    ecoe_id: UUID
    user_id: UUID


@command_handler
def add_ecoe_coordinator(
    command: AddEcoeCoordinatorCommand, repository: EcoeRepository
) -> CommandResult:
    ecoe: ECOE = repository.get_by_id(command.ecoe_id)
    coordinator: Coordinator = Coordinator(user_id=command.user_id)
    events = ecoe.add_coordinator(coordinator=coordinator)
    repository.update(ecoe)
    return CommandResult.ok(result=ecoe, events=events)
