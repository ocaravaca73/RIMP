"""
Telemetry collector for gathering and buffering telemetry data
"""
from datetime import datetime
from typing import Optional, List, Callable
from threading import Lock
import uuid

from .models import TelemetryEvent, TelemetryMetric, TelemetryData, EventType
from .config import TelemetryConfig


class TelemetryCollector:
    """
    Collects and buffers telemetry events and metrics
    
    Provides thread-safe collection and buffering of telemetry data
    with automatic flushing capabilities.
    """
    
    def __init__(self, config: Optional[TelemetryConfig] = None):
        """
        Initialize the telemetry collector
        
        Args:
            config: Telemetry configuration
        """
        self.config = config or TelemetryConfig()
        self.config.validate()
        
        self._buffer = TelemetryData()
        self._lock = Lock()
        self._listeners: List[Callable[[TelemetryData], None]] = []
    
    def collect_event(
        self,
        source: str,
        message: str,
        event_type: EventType = EventType.INFO,
        metadata: Optional[dict] = None
    ) -> TelemetryEvent:
        """
        Collect a telemetry event
        
        Args:
            source: Source of the event
            message: Event message
            event_type: Type of event
            metadata: Additional metadata
            
        Returns:
            The created telemetry event
        """
        if not self.config.enabled:
            return None
        
        event = TelemetryEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            event_type=event_type,
            source=source,
            message=message,
            metadata=metadata
        )
        
        with self._lock:
            self._buffer.add_event(event)
            
            if self.config.realtime_mode:
                self._notify_listeners()
            
            if len(self._buffer.events) >= self.config.buffer_size:
                self._flush()
        
        return event
    
    def collect_metric(
        self,
        name: str,
        value: float,
        unit: Optional[str] = None,
        tags: Optional[dict] = None
    ) -> TelemetryMetric:
        """
        Collect a telemetry metric
        
        Args:
            name: Metric name
            value: Metric value
            unit: Unit of measurement
            tags: Tags for filtering
            
        Returns:
            The created telemetry metric
        """
        if not self.config.enabled:
            return None
        
        metric = TelemetryMetric(
            metric_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            name=name,
            value=value,
            unit=unit,
            tags=tags
        )
        
        with self._lock:
            self._buffer.add_metric(metric)
            
            if self.config.realtime_mode:
                self._notify_listeners()
            
            if len(self._buffer.metrics) >= self.config.buffer_size:
                self._flush()
        
        return metric
    
    def add_listener(self, listener: Callable[[TelemetryData], None]) -> None:
        """
        Add a listener for real-time telemetry data
        
        Args:
            listener: Callback function that receives telemetry data
        """
        with self._lock:
            self._listeners.append(listener)
    
    def remove_listener(self, listener: Callable[[TelemetryData], None]) -> None:
        """
        Remove a listener
        
        Args:
            listener: Listener to remove
        """
        with self._lock:
            if listener in self._listeners:
                self._listeners.remove(listener)
    
    def flush(self) -> TelemetryData:
        """
        Manually flush the buffer
        
        Returns:
            The flushed telemetry data
        """
        with self._lock:
            return self._flush()
    
    def _flush(self) -> TelemetryData:
        """Internal flush implementation (must be called with lock held)"""
        data = self._buffer
        self._buffer = TelemetryData()
        return data
    
    def _notify_listeners(self) -> None:
        """Notify all listeners with current buffer data (must be called with lock held)"""
        if self._listeners and (self._buffer.events or self._buffer.metrics):
            # Create a snapshot of current data for listeners
            snapshot = TelemetryData(
                events=self._buffer.events.copy(),
                metrics=self._buffer.metrics.copy()
            )
            for listener in self._listeners:
                try:
                    listener(snapshot)
                except Exception:
                    # Silently ignore listener errors
                    pass
    
    def get_buffer_size(self) -> int:
        """Get current buffer size"""
        with self._lock:
            return len(self._buffer.events) + len(self._buffer.metrics)
