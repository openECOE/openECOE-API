from dataclasses import dataclass
from seedwork.domain.events import DomainEvent
from seedwork.domain.value_objects import UUID


class EcoeDraftCreatedEvent(DomainEvent):
    ecoe_id: UUID


class EcoeDraftUpdatedEvent(DomainEvent):
    ecoe_id: UUID


class EcoePublishedEvent(DomainEvent):
    ecoe_id: UUID
    

class EcoeArchivedEvent(DomainEvent):
    ecoe_id: UUID
    
class EcoeAddedCoordinatorEvent(DomainEvent):
    ecoe_id: UUID
    user_id: UUID
    
class EcoeRemovedCoordinatorEvent(DomainEvent):
    ecoe_id: UUID
    user_id: UUID