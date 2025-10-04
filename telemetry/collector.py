"""
Telemetry collector for gathering events and metrics.
"""

from datetime import datetime
from typing import List, Optional, Callable
from threading import Lock

from .models import TelemetryEvent, TelemetryMetric, TelemetryLevel, MetricType


class TelemetryCollector:
    """
    Central collector for telemetry data.
    
    Collects events and metrics from various sources and makes them
    available for streaming or batch processing.
    """
    
    def __init__(self, source: str = "default"):
        """
        Initialize the telemetry collector.
        
        Args:
            source: Default source identifier for events/metrics
        """
        self.source = source
        self._events: List[TelemetryEvent] = []
        self._metrics: List[TelemetryMetric] = []
        self._lock = Lock()
        self._event_handlers: List[Callable[[TelemetryEvent], None]] = []
        self._metric_handlers: List[Callable[[TelemetryMetric], None]] = []
    
    def collect_event(
        self,
        event_type: str,
        message: str = "",
        level: TelemetryLevel = TelemetryLevel.INFO,
        source: Optional[str] = None,
        **metadata
    ) -> TelemetryEvent:
        """
        Collect a telemetry event.
        
        Args:
            event_type: Type/category of the event
            message: Human-readable description
            level: Severity level
            source: Override default source
            **metadata: Additional contextual information
            
        Returns:
            The created TelemetryEvent
        """
        event = TelemetryEvent(
            timestamp=datetime.now(),
            source=source or self.source,
            event_type=event_type,
            level=level,
            message=message,
            metadata=metadata,
        )
        
        with self._lock:
            self._events.append(event)
        
        # Notify handlers
        for handler in self._event_handlers:
            handler(event)
        
        return event
    
    def collect_metric(
        self,
        name: str,
        value: float,
        metric_type: MetricType = MetricType.GAUGE,
        unit: Optional[str] = None,
        **tags
    ) -> TelemetryMetric:
        """
        Collect a telemetry metric.
        
        Args:
            name: Name of the metric
            value: Numeric value
            metric_type: Type of metric
            unit: Unit of measurement
            **tags: Dimension tags for the metric
            
        Returns:
            The created TelemetryMetric
        """
        metric = TelemetryMetric(
            timestamp=datetime.now(),
            name=name,
            value=value,
            metric_type=metric_type,
            unit=unit,
            tags=tags,
        )
        
        with self._lock:
            self._metrics.append(metric)
        
        # Notify handlers
        for handler in self._metric_handlers:
            handler(metric)
        
        return metric
    
    def get_events(self, limit: Optional[int] = None) -> List[TelemetryEvent]:
        """
        Get collected events.
        
        Args:
            limit: Maximum number of events to return (most recent)
            
        Returns:
            List of telemetry events
        """
        with self._lock:
            if limit:
                return self._events[-limit:]
            return self._events.copy()
    
    def get_metrics(self, limit: Optional[int] = None) -> List[TelemetryMetric]:
        """
        Get collected metrics.
        
        Args:
            limit: Maximum number of metrics to return (most recent)
            
        Returns:
            List of telemetry metrics
        """
        with self._lock:
            if limit:
                return self._metrics[-limit:]
            return self._metrics.copy()
    
    def clear(self):
        """Clear all collected events and metrics."""
        with self._lock:
            self._events.clear()
            self._metrics.clear()
    
    def on_event(self, handler: Callable[[TelemetryEvent], None]):
        """
        Register a handler for new events.
        
        Args:
            handler: Callback function that receives TelemetryEvent
        """
        self._event_handlers.append(handler)
    
    def on_metric(self, handler: Callable[[TelemetryMetric], None]):
        """
        Register a handler for new metrics.
        
        Args:
            handler: Callback function that receives TelemetryMetric
        """
        self._metric_handlers.append(handler)
