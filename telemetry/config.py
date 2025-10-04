"""
Configuration management for the telemetry system.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import json
import os


@dataclass
class TelemetryConfig:
    """
    Configuration for the telemetry system.
    
    Attributes:
        enabled: Whether telemetry is enabled
        source: Default source identifier
        buffer_size: Size of streaming buffer
        retention_limit: Maximum number of items to retain (None = unlimited)
        export_format: Format for exporting data (json, csv, etc.)
        export_path: Path for exporting telemetry data
        custom_settings: Additional custom configuration
    """
    enabled: bool = True
    source: str = "rimp"
    buffer_size: int = 1000
    retention_limit: Optional[int] = 10000
    export_format: str = "json"
    export_path: str = "./telemetry_data"
    custom_settings: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "TelemetryConfig":
        """
        Create a TelemetryConfig from a dictionary.
        
        Args:
            config_dict: Configuration dictionary
            
        Returns:
            TelemetryConfig instance
        """
        return cls(
            enabled=config_dict.get("enabled", True),
            source=config_dict.get("source", "rimp"),
            buffer_size=config_dict.get("buffer_size", 1000),
            retention_limit=config_dict.get("retention_limit", 10000),
            export_format=config_dict.get("export_format", "json"),
            export_path=config_dict.get("export_path", "./telemetry_data"),
            custom_settings=config_dict.get("custom_settings", {}),
        )
    
    @classmethod
    def from_file(cls, filepath: str) -> "TelemetryConfig":
        """
        Load configuration from a JSON file.
        
        Args:
            filepath: Path to configuration file
            
        Returns:
            TelemetryConfig instance
        """
        with open(filepath, "r") as f:
            config_dict = json.load(f)
        return cls.from_dict(config_dict)
    
    @classmethod
    def from_env(cls) -> "TelemetryConfig":
        """
        Load configuration from environment variables.
        
        Returns:
            TelemetryConfig instance
        """
        return cls(
            enabled=os.getenv("TELEMETRY_ENABLED", "true").lower() == "true",
            source=os.getenv("TELEMETRY_SOURCE", "rimp"),
            buffer_size=int(os.getenv("TELEMETRY_BUFFER_SIZE", "1000")),
            retention_limit=int(os.getenv("TELEMETRY_RETENTION_LIMIT", "10000")),
            export_format=os.getenv("TELEMETRY_EXPORT_FORMAT", "json"),
            export_path=os.getenv("TELEMETRY_EXPORT_PATH", "./telemetry_data"),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "enabled": self.enabled,
            "source": self.source,
            "buffer_size": self.buffer_size,
            "retention_limit": self.retention_limit,
            "export_format": self.export_format,
            "export_path": self.export_path,
            "custom_settings": self.custom_settings,
        }
    
    def to_file(self, filepath: str):
        """
        Save configuration to a JSON file.
        
        Args:
            filepath: Path to save configuration
        """
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
