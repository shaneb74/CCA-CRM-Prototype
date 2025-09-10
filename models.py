
from dataclasses import dataclass, asdict
from enum import Enum

class Origin(str, Enum):
    APP="app"; PHONE="phone"; HOSPITAL="hospital"

class Status(str, Enum):
    NEW="new"; IN_PROGRESS="in progress"; ACTIVE="active"

class Priority(str, Enum):
    HIGH="high"; MED="med"; LOW="low"

@dataclass
class Lead:
    id: str; name: str; origin: Origin; city: str
    preference: str=""; budget: int=0; timeline: str=""
    notes: str=""; assigned_to: str=""; status: Status=Status.NEW
    progress: float=0.0; ds_recommendation: str=""; ds_est_cost: int|float=0
    attrs: dict|None=None
    def to_dict(self): return asdict(self)

@dataclass
class Task:
    id: str; title: str; lead_id: str; priority: Priority
    due: object; origin: Origin; done: bool=False
    def to_dict(self): return asdict(self)

@dataclass
class Advisor:
    name: str
