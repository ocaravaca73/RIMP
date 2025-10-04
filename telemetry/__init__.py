"""
RIMP Real-Time Telemetry System

This module provides the core infrastructure for real-time telemetry collection,
processing, and streaming.
"""

__version__ = "0.1.0"

from .collector import TelemetryCollector
from .stream import TelemetryStream
from .models import TelemetryEvent, TelemetryMetric

__all__ = [
    "TelemetryCollector",
    "TelemetryStream",
    "TelemetryEvent",
    "TelemetryMetric",
]
