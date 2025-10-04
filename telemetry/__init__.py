"""
RIMP - Real-time Telemetry Infrastructure
ISBL Bootstrap Implementation

This package provides a foundation for real-time telemetry collection
and processing in the RIMP system.
"""

from telemetry.core import TelemetryService, DataCollector, TelemetryEvent
from telemetry.config import load_config, DEFAULT_CONFIG

__version__ = '0.1.0'
__all__ = [
    'TelemetryService',
    'DataCollector', 
    'TelemetryEvent',
    'load_config',
    'DEFAULT_CONFIG'
]
