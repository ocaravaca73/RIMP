"""
Real-time streaming for telemetry data
"""
from typing import Callable, List, Optional
from threading import Thread, Event
import time

from .models import TelemetryData
from .collector import TelemetryCollector
from .storage import TelemetryStorage


class TelemetryStream:
    """
    Real-time telemetry data stream
    
    Provides continuous streaming of telemetry data to consumers
    with configurable intervals and filtering.
    """
    
    def __init__(
        self,
        collector: TelemetryCollector,
        storage: Optional[TelemetryStorage] = None,
        interval: float = 1.0
    ):
        """
        Initialize the telemetry stream
        
        Args:
            collector: Telemetry collector to stream from
            storage: Optional storage backend
            interval: Streaming interval in seconds
        """
        self.collector = collector
        self.storage = storage
        self.interval = interval
        
        self._consumers: List[Callable[[TelemetryData], None]] = []
        self._stop_event = Event()
        self._thread: Optional[Thread] = None
    
    def add_consumer(self, consumer: Callable[[TelemetryData], None]) -> None:
        """
        Add a consumer for the stream
        
        Args:
            consumer: Callback function that processes telemetry data
        """
        self._consumers.append(consumer)
    
    def remove_consumer(self, consumer: Callable[[TelemetryData], None]) -> None:
        """
        Remove a consumer from the stream
        
        Args:
            consumer: Consumer to remove
        """
        if consumer in self._consumers:
            self._consumers.remove(consumer)
    
    def start(self) -> None:
        """Start the telemetry stream"""
        if self._thread and self._thread.is_alive():
            return
        
        self._stop_event.clear()
        self._thread = Thread(target=self._stream_loop, daemon=True)
        self._thread.start()
        
        # Also register as a real-time listener with the collector
        if self.collector.config.realtime_mode:
            self.collector.add_listener(self._on_realtime_data)
    
    def stop(self) -> None:
        """Stop the telemetry stream"""
        self._stop_event.set()
        
        if self._thread:
            self._thread.join(timeout=5.0)
            self._thread = None
        
        # Unregister listener
        self.collector.remove_listener(self._on_realtime_data)
    
    def _stream_loop(self) -> None:
        """Main streaming loop"""
        while not self._stop_event.is_set():
            # Flush collector buffer periodically
            data = self.collector.flush()
            
            if data.events or data.metrics:
                # Store if storage backend is available
                if self.storage:
                    try:
                        self.storage.store(data)
                    except Exception:
                        pass
                
                # Send to consumers
                self._send_to_consumers(data)
            
            # Wait for next interval
            self._stop_event.wait(self.interval)
    
    def _on_realtime_data(self, data: TelemetryData) -> None:
        """Handle real-time data from collector"""
        self._send_to_consumers(data)
    
    def _send_to_consumers(self, data: TelemetryData) -> None:
        """Send data to all consumers"""
        for consumer in self._consumers:
            try:
                consumer(data)
            except Exception:
                # Silently ignore consumer errors
                pass
