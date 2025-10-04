"""
Real-time telemetry streaming infrastructure.
"""

from typing import List, Optional, Callable, Any
from threading import Thread, Event
from queue import Queue, Empty
import time

from .models import TelemetryEvent, TelemetryMetric


class TelemetryStream:
    """
    Real-time streaming interface for telemetry data.
    
    Provides mechanisms to stream telemetry events and metrics
    to consumers in real-time.
    """
    
    def __init__(self, buffer_size: int = 1000):
        """
        Initialize the telemetry stream.
        
        Args:
            buffer_size: Maximum size of the internal buffer
        """
        self._event_queue: Queue = Queue(maxsize=buffer_size)
        self._metric_queue: Queue = Queue(maxsize=buffer_size)
        self._subscribers: List[Callable[[Any], None]] = []
        self._running = False
        self._stop_event = Event()
        self._worker_thread: Optional[Thread] = None
    
    def push_event(self, event: TelemetryEvent):
        """
        Push an event to the stream.
        
        Args:
            event: TelemetryEvent to stream
        """
        try:
            self._event_queue.put_nowait(event)
        except:
            # Queue is full, drop oldest
            try:
                self._event_queue.get_nowait()
                self._event_queue.put_nowait(event)
            except:
                pass
    
    def push_metric(self, metric: TelemetryMetric):
        """
        Push a metric to the stream.
        
        Args:
            metric: TelemetryMetric to stream
        """
        try:
            self._metric_queue.put_nowait(metric)
        except:
            # Queue is full, drop oldest
            try:
                self._metric_queue.get_nowait()
                self._metric_queue.put_nowait(metric)
            except:
                pass
    
    def subscribe(self, callback: Callable[[Any], None]):
        """
        Subscribe to the telemetry stream.
        
        Args:
            callback: Function to call with each telemetry item
        """
        self._subscribers.append(callback)
    
    def start(self):
        """Start the streaming worker."""
        if self._running:
            return
        
        self._running = True
        self._stop_event.clear()
        self._worker_thread = Thread(target=self._stream_worker, daemon=True)
        self._worker_thread.start()
    
    def stop(self):
        """Stop the streaming worker."""
        if not self._running:
            return
        
        self._running = False
        self._stop_event.set()
        
        if self._worker_thread:
            self._worker_thread.join(timeout=5)
    
    def _stream_worker(self):
        """Worker thread that processes the stream."""
        while self._running and not self._stop_event.is_set():
            # Process events
            try:
                event = self._event_queue.get(timeout=0.1)
                self._notify_subscribers(event)
            except Empty:
                pass
            
            # Process metrics
            try:
                metric = self._metric_queue.get(timeout=0.1)
                self._notify_subscribers(metric)
            except Empty:
                pass
    
    def _notify_subscribers(self, item: Any):
        """Notify all subscribers of a new item."""
        for subscriber in self._subscribers:
            try:
                subscriber(item)
            except Exception:
                # Don't let subscriber errors break the stream
                pass
    
    def get_pending_count(self) -> tuple:
        """
        Get the number of pending items in the stream.
        
        Returns:
            Tuple of (event_count, metric_count)
        """
        return (self._event_queue.qsize(), self._metric_queue.qsize())
