# models.py — tiny model layer for safety + extensibility
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, Dict, Any
from datetime import date

class Origin(str, Enum):
    APP = "app"
    PHONE = "phone"
    HOSPITAL = "hospital"

class Status(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

class Priority(str, Enum):
    HIGH = "High"
    MED = "Med"
    LOW = "Low"

@dataclass
class Advisor:
    id: str
    name: str
    email: Optional[str] = None
    region: Optional[str] = None
    attrs: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class Lead:
    id: str
    name: str
    origin: Origin
    city: str
    preference: Optional[str] = None
    budget: Optional[int] = None
    timeline: Optional[str] = None
    notes: Optional[str] = None
    created: date = field(default_factory=date.today)
    assigned_to: Optional[str] = None  # advisor name or id
    status: Status = Status.NEW
    progress: float = 0.0
    ds_recommendation: Optional[str] = None
    ds_est_cost: Optional[int] = None
    attrs: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["origin"] = self.origin.value
        d["status"] = self.status.value
        return d

@dataclass
class Task:
    id: str
    title: str
    lead_id: str
    priority: Priority
    due: date
    origin: Origin
    done: bool = False
    attrs: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["priority"] = self.priority.value
        d["origin"] = self.origin.value
        return d
