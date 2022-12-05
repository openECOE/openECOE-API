from modules.manage.ecoe.application.command.add_ecoe_coordinator import AddEcoeCoordinatorCommand, add_ecoe_coordinator
from modules.manage.ecoe.domain.repositories import EcoeRepository
from seedwork.application.modules import BusinessModule
from seedwork.domain.events import EventPublisher

from modules.manage.ecoe.application.query.get_all_ecoes import GetAllEcoes, get_all_ecoes
from modules.manage.ecoe.application.query.get_ecoe_details import GetEcoeDetails, get_ecoe_details

from modules.manage.ecoe.application.command.archive_ecoe import ArchiveEcoeCommand, archive_ecoe_draft
from modules.manage.ecoe.application.command.create_ecoe_draft import CreateEcoeDraftCommand, create_ecoe_draft
from modules.manage.ecoe.application.command.publish_ecoe import PublishEcoeDraftCommand, publish_ecoe_draft
from modules.manage.ecoe.application.command.update_ecoe_draft import UpdateEcoeDraftCommand, update_ecoe_draft

class ManageModule(BusinessModule):
    query_handlers = {
        GetAllEcoes: lambda self, q: get_all_ecoes(q, repository=self.ecoe_repository),
        GetEcoeDetails: lambda self, q: get_ecoe_details(q, repository=self.ecoe_repository),
    }
    command_handlers = {
        CreateEcoeDraftCommand: lambda self, c: create_ecoe_draft(c, repository=self.ecoe_repository),
        UpdateEcoeDraftCommand: lambda self, c: update_ecoe_draft(c, repository=self.ecoe_repository),
        PublishEcoeDraftCommand: lambda self, c: publish_ecoe_draft(c, repository=self.ecoe_repository),
        ArchiveEcoeCommand: lambda self, c: archive_ecoe_draft(c, repository=self.ecoe_repository),
        AddEcoeCoordinatorCommand: lambda self, c: add_ecoe_coordinator(c, repository=self.ecoe_repository)
    }

    def __init__(
        self,
        ecoe_repository: EcoeRepository,
    ) -> None:
        self.ecoe_repository = ecoe_repository

    @staticmethod
    def create(container):
        """Factory method for creating a module by using dependencies from a DI container"""
        return ManageModule(
            logger=container.logger(),
            ecoe_repository=container.ecoe_repository(),
        )