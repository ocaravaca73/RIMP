"""
Telemetry data models for the RIMP real-time telemetry system.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class TelemetryLevel(Enum):
    """Telemetry event severity levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class MetricType(Enum):
    """Types of metrics that can be collected."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


@dataclass
class TelemetryEvent:
    """
    Represents a telemetry event in the system.
    
    Attributes:
        timestamp: When the event occurred
        source: Origin of the event (service, component, etc.)
        event_type: Type/category of the event
        level: Severity level of the event
        message: Human-readable description
        metadata: Additional contextual information
    """
    timestamp: datetime
    source: str
    event_type: str
    level: TelemetryLevel = TelemetryLevel.INFO
    message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "event_type": self.event_type,
            "level": self.level.value,
            "message": self.message,
            "metadata": self.metadata,
        }


@dataclass
class TelemetryMetric:
    """
    Represents a telemetry metric in the system.
    
    Attributes:
        timestamp: When the metric was recorded
        name: Name of the metric
        value: Numeric value of the metric
        metric_type: Type of metric (counter, gauge, etc.)
        unit: Unit of measurement (optional)
        tags: Key-value pairs for metric dimensions
    """
    timestamp: datetime
    name: str
    value: float
    metric_type: MetricType = MetricType.GAUGE
    unit: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the metric to a dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "name": self.name,
            "value": self.value,
            "metric_type": self.metric_type.value,
            "unit": self.unit,
            "tags": self.tags,
        }
