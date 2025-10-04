"""
Telemetry configuration
"""
from typing import Optional
from dataclasses import dataclass


@dataclass
class TelemetryConfig:
    """
    Configuration for the telemetry system
    
    Attributes:
        enabled: Whether telemetry is enabled
        buffer_size: Maximum number of items in buffer before flushing
        flush_interval: Interval in seconds for automatic flushing
        realtime_mode: Enable real-time streaming mode
        storage_backend: Storage backend type (memory, file, database)
        storage_path: Path for file-based storage
    """
    enabled: bool = True
    buffer_size: int = 100
    flush_interval: float = 5.0
    realtime_mode: bool = True
    storage_backend: str = "memory"
    storage_path: Optional[str] = None
    
    def validate(self) -> None:
        """Validate configuration"""
        if self.buffer_size <= 0:
            raise ValueError("buffer_size must be positive")
        if self.flush_interval <= 0:
            raise ValueError("flush_interval must be positive")
        if self.storage_backend not in ["memory", "file", "database"]:
            raise ValueError(f"Invalid storage_backend: {self.storage_backend}")
