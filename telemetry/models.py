"""
Telemetry Data Models

Defines the core data structures for telemetry: Metrics, Events, and Traces.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum


class MetricType(Enum):
    """Types of metrics that can be collected."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"


class EventSeverity(Enum):
    """Severity levels for events."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class Metric:
    """
    Represents a telemetry metric.
    
    Attributes:
        name: Metric name
        value: Metric value
        metric_type: Type of metric (counter, gauge, histogram)
        timestamp: When the metric was recorded
        tags: Additional metadata tags
    """
    name: str
    value: float
    metric_type: MetricType = MetricType.GAUGE
    timestamp: datetime = field(default_factory=datetime.utcnow)
    tags: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metric to dictionary format."""
        return {
            "name": self.name,
            "value": self.value,
            "type": self.metric_type.value,
            "timestamp": self.timestamp.isoformat(),
            "tags": self.tags
        }


@dataclass
class Event:
    """
    Represents a telemetry event.
    
    Attributes:
        name: Event name
        message: Event message
        severity: Event severity level
        timestamp: When the event occurred
        metadata: Additional event metadata
    """
    name: str
    message: str
    severity: EventSeverity = EventSeverity.INFO
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary format."""
        return {
            "name": self.name,
            "message": self.message,
            "severity": self.severity.value,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


@dataclass
class Trace:
    """
    Represents a telemetry trace for distributed tracing.
    
    Attributes:
        trace_id: Unique trace identifier
        span_id: Unique span identifier
        operation: Operation name
        start_time: When the operation started
        duration_ms: Operation duration in milliseconds
        parent_span_id: Parent span ID for nested operations
        tags: Additional trace tags
    """
    trace_id: str
    span_id: str
    operation: str
    start_time: datetime = field(default_factory=datetime.utcnow)
    duration_ms: Optional[float] = None
    parent_span_id: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert trace to dictionary format."""
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "operation": self.operation,
            "start_time": self.start_time.isoformat(),
            "duration_ms": self.duration_ms,
            "parent_span_id": self.parent_span_id,
            "tags": self.tags
        }
