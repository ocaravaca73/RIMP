"""
Telemetry data models
"""
from datetime import datetime
from typing import Any, Dict, Optional, List
from enum import Enum

try:
    from pydantic import BaseModel, Field
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    # Fallback for environments without pydantic
    class BaseModel:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
        
        def dict(self):
            return self.__dict__
    
    def Field(**kwargs):
        default = kwargs.get('default', None)
        default_factory = kwargs.get('default_factory', None)
        if default_factory:
            return default_factory()
        return default


class EventType(str, Enum):
    """Types of telemetry events"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    DEBUG = "debug"


class TelemetryEvent(BaseModel):
    """
    Represents a telemetry event
    
    Attributes:
        event_id: Unique identifier for the event
        timestamp: When the event occurred
        event_type: Type of event (info, warning, error, debug)
        source: Source system or component that generated the event
        message: Event message
        metadata: Additional event metadata
    """
    event_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow) if PYDANTIC_AVAILABLE else None
    event_type: EventType = EventType.INFO
    source: str
    message: str
    metadata: Optional[Dict[str, Any]] = None
    
    def __init__(self, **kwargs):
        if not PYDANTIC_AVAILABLE:
            self.event_id = kwargs.get('event_id')
            self.timestamp = kwargs.get('timestamp', datetime.utcnow())
            self.event_type = kwargs.get('event_type', EventType.INFO)
            self.source = kwargs.get('source')
            self.message = kwargs.get('message')
            self.metadata = kwargs.get('metadata')
        else:
            super().__init__(**kwargs)


class TelemetryMetric(BaseModel):
    """
    Represents a telemetry metric
    
    Attributes:
        metric_id: Unique identifier for the metric
        timestamp: When the metric was recorded
        name: Metric name
        value: Metric value
        unit: Unit of measurement
        tags: Tags for filtering and grouping
    """
    metric_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow) if PYDANTIC_AVAILABLE else None
    name: str
    value: float
    unit: Optional[str] = None
    tags: Optional[Dict[str, str]] = None
    
    def __init__(self, **kwargs):
        if not PYDANTIC_AVAILABLE:
            self.metric_id = kwargs.get('metric_id')
            self.timestamp = kwargs.get('timestamp', datetime.utcnow())
            self.name = kwargs.get('name')
            self.value = kwargs.get('value')
            self.unit = kwargs.get('unit')
            self.tags = kwargs.get('tags')
        else:
            super().__init__(**kwargs)


class TelemetryData(BaseModel):
    """
    Container for telemetry data (events and metrics)
    
    Attributes:
        events: List of telemetry events
        metrics: List of telemetry metrics
    """
    events: List[TelemetryEvent] = Field(default_factory=list) if PYDANTIC_AVAILABLE else None
    metrics: List[TelemetryMetric] = Field(default_factory=list) if PYDANTIC_AVAILABLE else None
    
    def __init__(self, **kwargs):
        if not PYDANTIC_AVAILABLE:
            self.events = kwargs.get('events', [])
            self.metrics = kwargs.get('metrics', [])
        else:
            super().__init__(**kwargs)
    
    def add_event(self, event: TelemetryEvent) -> None:
        """Add an event to the telemetry data"""
        self.events.append(event)
    
    def add_metric(self, metric: TelemetryMetric) -> None:
        """Add a metric to the telemetry data"""
        self.metrics.append(metric)
