"""
Real-time Telemetry Module

This module provides the foundation for collecting, processing, and streaming
telemetry data in real-time.
"""

from .collector import TelemetryCollector
from .models import Metric, Event, Trace
from .config import TelemetryConfig

__version__ = "0.1.0"
__all__ = ["TelemetryCollector", "Metric", "Event", "Trace", "TelemetryConfig"]
