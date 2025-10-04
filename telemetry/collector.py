"""
Telemetry Collector

Core component for collecting and processing telemetry data in real-time.
"""

import threading
import time
import queue
import random
from typing import List, Callable, Optional
from datetime import datetime

from .models import Metric, Event, Trace
from .config import TelemetryConfig


class TelemetryCollector:
    """
    Collects, buffers, and processes telemetry data in real-time.
    
    This class manages a buffer of telemetry data and periodically flushes it
    to registered exporters. It runs in a background thread for real-time processing.
    """
    
    def __init__(self, config: Optional[TelemetryConfig] = None):
        """
        Initialize the telemetry collector.
        
        Args:
            config: Configuration for the collector. Uses defaults if not provided.
        """
        self.config = config or TelemetryConfig()
        self.config.validate()
        
        self._buffer: queue.Queue = queue.Queue(maxsize=self.config.buffer_size)
        self._exporters: List[Callable] = []
        self._running = False
        self._flush_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        
    def start(self) -> None:
        """Start the telemetry collector background thread."""
        if self._running:
            return
            
        self._running = True
        self._flush_thread = threading.Thread(target=self._flush_loop, daemon=True)
        self._flush_thread.start()
        
    def stop(self) -> None:
        """Stop the telemetry collector and flush remaining data."""
        if not self._running:
            return
            
        self._running = False
        if self._flush_thread:
            self._flush_thread.join(timeout=5)
        
        # Flush any remaining data
        self._flush()
        
    def collect_metric(self, metric: Metric) -> None:
        """
        Collect a metric.
        
        Args:
            metric: The metric to collect
        """
        if not self.config.enabled:
            return
            
        if not self._should_sample():
            return
            
        # Apply global tags
        metric.tags.update(self.config.tags)
        
        try:
            self._buffer.put_nowait(("metric", metric))
        except queue.Full:
            # Buffer is full, drop the metric
            pass
            
    def collect_event(self, event: Event) -> None:
        """
        Collect an event.
        
        Args:
            event: The event to collect
        """
        if not self.config.enabled:
            return
            
        if not self._should_sample():
            return
            
        # Apply global metadata
        event.metadata.update(self.config.tags)
        
        try:
            self._buffer.put_nowait(("event", event))
        except queue.Full:
            pass
            
    def collect_trace(self, trace: Trace) -> None:
        """
        Collect a trace.
        
        Args:
            trace: The trace to collect
        """
        if not self.config.enabled:
            return
            
        if not self._should_sample():
            return
            
        # Apply global tags
        trace.tags.update(self.config.tags)
        
        try:
            self._buffer.put_nowait(("trace", trace))
        except queue.Full:
            pass
            
    def register_exporter(self, exporter: Callable) -> None:
        """
        Register an exporter function to process telemetry data.
        
        Args:
            exporter: A callable that accepts (data_type, data) and processes it
        """
        with self._lock:
            self._exporters.append(exporter)
            
    def _should_sample(self) -> bool:
        """Determine if this telemetry item should be sampled."""
        return random.random() < self.config.sample_rate
        
    def _flush_loop(self) -> None:
        """Background thread that periodically flushes telemetry data."""
        while self._running:
            time.sleep(self.config.flush_interval_ms / 1000.0)
            self._flush()
            
    def _flush(self) -> None:
        """Flush buffered telemetry data to exporters."""
        items = []
        
        # Drain the queue
        while not self._buffer.empty():
            try:
                items.append(self._buffer.get_nowait())
            except queue.Empty:
                break
                
        if not items:
            return
            
        # Export to all registered exporters
        with self._lock:
            for exporter in self._exporters:
                try:
                    for data_type, data in items:
                        exporter(data_type, data)
                except Exception as e:
                    # Log error but continue with other exporters
                    print(f"Exporter error: {e}")
