"""
Telemetry Configuration

Manages configuration for the telemetry system.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TelemetryConfig:
    """
    Configuration for telemetry system.
    
    Attributes:
        enabled: Whether telemetry collection is enabled
        buffer_size: Size of the telemetry buffer
        flush_interval_ms: Interval to flush telemetry data (milliseconds)
        export_endpoints: List of endpoints to export telemetry data
        sample_rate: Sampling rate for telemetry (0.0 to 1.0)
        tags: Global tags to apply to all telemetry
    """
    enabled: bool = True
    buffer_size: int = 1000
    flush_interval_ms: int = 5000
    export_endpoints: List[str] = field(default_factory=list)
    sample_rate: float = 1.0
    tags: dict = field(default_factory=dict)
    
    def validate(self) -> None:
        """Validate configuration parameters."""
        if self.buffer_size <= 0:
            raise ValueError("buffer_size must be positive")
        if self.flush_interval_ms <= 0:
            raise ValueError("flush_interval_ms must be positive")
        if not 0.0 <= self.sample_rate <= 1.0:
            raise ValueError("sample_rate must be between 0.0 and 1.0")
