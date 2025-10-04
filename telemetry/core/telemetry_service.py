"""
Telemetry Service
Main service for managing real-time telemetry
"""

from typing import Dict, Any, Optional
from .data_collector import DataCollector
from .telemetry_event import TelemetryEvent


class TelemetryService:
    """
    Main telemetry service for real-time data collection and processing.
    Provides a high-level interface for telemetry operations.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the telemetry service.
        
        Args:
            config: Configuration dictionary
        """
        self._config = config or {}
        self._enabled = self._config.get('enabled', True)
        self._buffer_size = self._config.get('buffer_size', 1000)
        self._collector = DataCollector(max_buffer_size=self._buffer_size)
        self._running = False
    
    def start(self) -> None:
        """Start the telemetry service"""
        if self._enabled:
            self._running = True
    
    def stop(self) -> None:
        """Stop the telemetry service"""
        self._running = False
    
    def emit(self, event_type: str, source: str, data: Dict[str, Any], 
             metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Emit a telemetry event.
        
        Args:
            event_type: Type of event
            source: Source system/component
            data: Event data
            metadata: Optional metadata
            
        Returns:
            True if event was emitted successfully
        """
        if not self._enabled or not self._running:
            return False
        
        event = TelemetryEvent(
            event_type=event_type,
            source=source,
            data=data,
            metadata=metadata or {}
        )
        
        return self._collector.collect(event)
    
    def get_events(self, batch_size: int = 10) -> list:
        """
        Retrieve collected events.
        
        Args:
            batch_size: Maximum number of events to retrieve
            
        Returns:
            List of event dictionaries
        """
        events = self._collector.retrieve(batch_size=batch_size)
        return [event.to_dict() for event in events]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get service statistics"""
        stats = self._collector.get_stats()
        stats.update({
            'enabled': self._enabled,
            'running': self._running,
            'config': self._config
        })
        return stats
    
    def is_running(self) -> bool:
        """Check if service is running"""
        return self._running
