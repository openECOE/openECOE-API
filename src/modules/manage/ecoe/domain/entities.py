from dataclasses import dataclass, field
from typing import List, Optional
from modules.manage.ecoe.domain.events import \
    EcoeDraftUpdatedEvent, EcoePublishedEvent, EcoeArchivedEvent, \
    EcoeAddedCoordinatorEvent, EcoeRemovedCoordinatorEvent

from seedwork.domain.entities import AggregateRoot
from seedwork.domain.events import DomainEvent
from seedwork.domain.value_objects import UUID
from .value_objects import Coordinator, Round, Shift, Status

@dataclass
class ECOE(AggregateRoot):
    id: UUID
    name: str = ""
    status: Status = Status.DRAFT
    coordinators: Optional[List[Coordinator]] = field(default_factory=list)
    rounds: Optional[List[Round]] = field(default_factory=list)
    shifts: Optional[List[Shift]] = field(default_factory=list)
    
        
    def change_main_attributes(self, name: str) -> List[DomainEvent]:
        self.name = name
        
        return [EcoeDraftUpdatedEvent(ecoe_id=self.id)]
            
    def publish(self) -> List[DomainEvent]:
        self.status = Status.PUBLISHED
        return [EcoePublishedEvent(ecoe_id=self.id)]
    
    def draft(self) -> List[DomainEvent]:
        self.status = Status.DRAFT
        return [EcoeDraftUpdatedEvent(ecoe_id=self.id)]
    
    def archive(self) -> List[DomainEvent]:
        self.status = Status.ARCHIVED
        return [EcoeArchivedEvent(ecoe_id=self.id)]
        
    def add_coordinator(self, coordinator: Coordinator) -> List[DomainEvent]:
        self.coordinators.append(coordinator)
        return [EcoeAddedCoordinatorEvent(ecoe_id=self.id, user_id=coordinator.user_id)]
        
    def del_coordinator(self, coordinator: Coordinator) -> List[DomainEvent]:
        self.coordinators.remove(coordinator)
        return [EcoeRemovedCoordinatorEvent(ecoe_id=self.id, user_id=coordinator.user_id)]
        
    def add_round(self, round: Round) -> List[DomainEvent]:
        self.rounds.append(round)
        # TODO: Añadir Evento a devolver
        
    def del_round(self, round: Round) -> List[DomainEvent]:
        self.rounds.remove(round)
        # TODO: Añadir Evento a devolver
        
    def add_shift(self, shift: Shift) -> List[DomainEvent]:
        self.shifts.append(shift)
        # TODO: Añadir Evento a devolver
        
    def del_shift(self, shift: Shift) -> List[DomainEvent]:
        self.shifts.remove(shift)
        # TODO: Añadir Evento a devolver
    
    def is_coordinator(self, coordinator: Coordinator) -> bool:
        try:
            self.coordinators.index(coordinator)
        except ValueError:
            return False
        return True