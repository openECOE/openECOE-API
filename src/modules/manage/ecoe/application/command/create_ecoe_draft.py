from seedwork.application.commands import Command
from seedwork.application.command_handlers import CommandResult
from seedwork.application.decorators import command_handler
from modules.manage.ecoe.domain.entities import ECOE
from modules.manage.ecoe.domain.events import EcoeDraftCreatedEvent
from modules.manage.ecoe.domain.repositories import EcoeRepository


class CreateEcoeDraftCommand(Command):
    """A command for creating new ecoe in draft state"""

    name: str


@command_handler
def create_ecoe_draft(
        command: CreateEcoeDraftCommand, repository: EcoeRepository
) -> CommandResult:
    ecoe = ECOE(id=ECOE.next_id(), **command.dict())
    repository.insert(ecoe)
    return CommandResult.ok(result=ecoe, events=[EcoeDraftCreatedEvent(ecoe_id=ecoe.id)])
