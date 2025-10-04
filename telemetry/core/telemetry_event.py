"""
Telemetry Event Data Structure
Defines the schema for telemetry events
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional
import uuid


@dataclass
class TelemetryEvent:
    """
    Represents a single telemetry event in the real-time system.
    
    Attributes:
        event_id: Unique identifier for the event
        timestamp: When the event occurred
        event_type: Type/category of the event
        source: Source system or component
        data: Event payload data
        metadata: Additional metadata
    """
    event_type: str
    source: str
    data: Dict[str, Any]
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary representation"""
        return {
            'event_id': self.event_id,
            'timestamp': self.timestamp.isoformat(),
            'event_type': self.event_type,
            'source': self.source,
            'data': self.data,
            'metadata': self.metadata
        }
