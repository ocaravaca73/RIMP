"""
Data models for telemetry system.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone


class ProjectType(Enum):
    """Project type enumeration."""
    FEATURE = "Feature"
    BUG = "Bug"
    TASK = "Task"
    EPIC = "Epic"


class Priority(Enum):
    """Priority enumeration."""
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class Area(Enum):
    """Area enumeration."""
    REALTIME = "Realtime"
    BACKEND = "Backend"
    FRONTEND = "Frontend"
    INFRASTRUCTURE = "Infrastructure"


@dataclass
class Project:
    """Project data model with required fields."""
    
    title: str
    type: ProjectType
    priority: Priority
    area: Area
    sprint: str
    estimate: int
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize created_at if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
    
    def to_dict(self):
        """Convert project to dictionary."""
        return {
            'title': self.title,
            'type': self.type.value,
            'priority': self.priority.value,
            'area': self.area.value,
            'sprint': self.sprint,
            'estimate': self.estimate,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
