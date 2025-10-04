"""
Data Collector Interface
Handles collection and buffering of telemetry data
"""

from typing import List, Optional, Callable
from queue import Queue, Empty
from threading import Lock
from .telemetry_event import TelemetryEvent


class DataCollector:
    """
    Collects and buffers telemetry events for real-time processing.
    Thread-safe implementation with configurable buffer size.
    """
    
    def __init__(self, max_buffer_size: int = 1000):
        """
        Initialize the data collector.
        
        Args:
            max_buffer_size: Maximum number of events to buffer
        """
        self._buffer = Queue(maxsize=max_buffer_size)
        self._lock = Lock()
        self._event_count = 0
        self._callbacks: List[Callable[[TelemetryEvent], None]] = []
    
    def collect(self, event: TelemetryEvent) -> bool:
        """
        Collect a telemetry event.
        
        Args:
            event: TelemetryEvent to collect
            
        Returns:
            True if event was collected, False if buffer is full
        """
        try:
            self._buffer.put_nowait(event)
            with self._lock:
                self._event_count += 1
            
            # Notify callbacks
            for callback in self._callbacks:
                try:
                    callback(event)
                except Exception:
                    pass  # Don't let callback errors affect collection
            
            return True
        except Exception:
            return False
    
    def retrieve(self, batch_size: int = 10, timeout: float = 0.1) -> List[TelemetryEvent]:
        """
        Retrieve events from the buffer.
        
        Args:
            batch_size: Maximum number of events to retrieve
            timeout: Timeout for waiting on empty buffer
            
        Returns:
            List of TelemetryEvent objects
        """
        events = []
        for _ in range(batch_size):
            try:
                event = self._buffer.get(timeout=timeout)
                events.append(event)
            except Empty:
                break
        return events
    
    def register_callback(self, callback: Callable[[TelemetryEvent], None]) -> None:
        """Register a callback to be called when events are collected"""
        self._callbacks.append(callback)
    
    def get_stats(self) -> dict:
        """Get collector statistics"""
        return {
            'total_events_collected': self._event_count,
            'current_buffer_size': self._buffer.qsize(),
            'max_buffer_size': self._buffer.maxsize
        }
