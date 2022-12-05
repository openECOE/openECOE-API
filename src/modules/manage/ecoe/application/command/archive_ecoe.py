from seedwork.application.commands import Command
from seedwork.application.command_handlers import CommandResult
from seedwork.application.decorators import command_handler
from seedwork.domain.value_objects import UUID
from modules.manage.ecoe.domain.entities import ECOE
from modules.manage.ecoe.domain.repositories import EcoeRepository


class ArchiveEcoeCommand(Command):
    """A command for updating a listing"""

    ecoe_id: UUID
    # modify_user_id: UUID


@command_handler
def archive_ecoe_draft(
    command: ArchiveEcoeCommand, repository: EcoeRepository
) -> CommandResult:
    ecoe: ECOE = repository.get_by_id(command.ecoe_id)
    events = ecoe.archive()
    repository.update(ecoe)
    return CommandResult.ok(result=ecoe, events=events)