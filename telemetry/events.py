"""
Real-time event system for telemetry.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List
from enum import Enum


class EventType(Enum):
    """Event type enumeration."""
    PROJECT_CREATED = "project.created"
    PROJECT_UPDATED = "project.updated"
    PROJECT_DELETED = "project.deleted"
    TASK_CREATED = "task.created"
    TASK_UPDATED = "task.updated"
    TASK_COMPLETED = "task.completed"


@dataclass
class TelemetryEvent:
    """Telemetry event data structure."""
    
    event_type: EventType
    data: Dict[str, Any]
    timestamp: datetime = None
    
    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)
    
    def to_dict(self):
        """Convert event to dictionary."""
        return {
            'event_type': self.event_type.value,
            'data': self.data,
            'timestamp': self.timestamp.isoformat()
        }


class EventEmitter:
    """Real-time event emitter for telemetry system."""
    
    def __init__(self):
        """Initialize event emitter."""
        self._listeners: Dict[EventType, List[Callable]] = {}
        self._events: List[TelemetryEvent] = []
    
    def on(self, event_type: EventType, callback: Callable):
        """Register event listener."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)
    
    def emit(self, event: TelemetryEvent):
        """Emit event to all registered listeners."""
        self._events.append(event)
        
        if event.event_type in self._listeners:
            for callback in self._listeners[event.event_type]:
                callback(event)
    
    def get_events(self, event_type: EventType = None) -> List[TelemetryEvent]:
        """Get all events or events of specific type."""
        if event_type is None:
            return self._events.copy()
        return [e for e in self._events if e.event_type == event_type]
    
    def clear(self):
        """Clear all stored events."""
        self._events.clear()
