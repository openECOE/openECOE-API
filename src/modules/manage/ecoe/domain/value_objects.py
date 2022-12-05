from dataclasses import dataclass, field
from datetime import date, time
from typing import List, Optional
from uuid import UUID
from seedwork.domain.value_objects import ValueObject

@dataclass
class Status(ValueObject):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


@dataclass
class Coordinator(ValueObject):
    user_id: UUID


@dataclass    
class Timer(ValueObject):
    pass


@dataclass    
class Round(ValueObject):
    name: str
    code: str
    

@dataclass
class Shift(ValueObject):
    code: str
    day: date
    times: List[time] = field(default_factory=list)
