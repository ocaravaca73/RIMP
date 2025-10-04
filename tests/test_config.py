"""
Tests for telemetry configuration.
"""

import unittest
from telemetry.config import TelemetryConfig


class TestTelemetryConfig(unittest.TestCase):
    """Test cases for TelemetryConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = TelemetryConfig()
        self.assertTrue(config.enabled)
        self.assertEqual(config.buffer_size, 1000)
        self.assertEqual(config.flush_interval_ms, 5000)
        self.assertEqual(config.export_endpoints, [])
        self.assertEqual(config.sample_rate, 1.0)
        self.assertEqual(config.tags, {})
        
    def test_custom_config(self):
        """Test custom configuration values."""
        config = TelemetryConfig(
            enabled=False,
            buffer_size=500,
            flush_interval_ms=1000,
            export_endpoints=["http://localhost:8080"],
            sample_rate=0.5,
            tags={"env": "test"}
        )
        self.assertFalse(config.enabled)
        self.assertEqual(config.buffer_size, 500)
        self.assertEqual(config.flush_interval_ms, 1000)
        self.assertEqual(config.export_endpoints, ["http://localhost:8080"])
        self.assertEqual(config.sample_rate, 0.5)
        self.assertEqual(config.tags, {"env": "test"})
        
    def test_validate_buffer_size(self):
        """Test validation of buffer size."""
        config = TelemetryConfig(buffer_size=-1)
        with self.assertRaises(ValueError) as context:
            config.validate()
        self.assertIn("buffer_size must be positive", str(context.exception))
        
    def test_validate_flush_interval(self):
        """Test validation of flush interval."""
        config = TelemetryConfig(flush_interval_ms=0)
        with self.assertRaises(ValueError) as context:
            config.validate()
        self.assertIn("flush_interval_ms must be positive", str(context.exception))
        
    def test_validate_sample_rate(self):
        """Test validation of sample rate."""
        config = TelemetryConfig(sample_rate=1.5)
        with self.assertRaises(ValueError) as context:
            config.validate()
        self.assertIn("sample_rate must be between 0.0 and 1.0", str(context.exception))
        
        config = TelemetryConfig(sample_rate=-0.1)
        with self.assertRaises(ValueError) as context:
            config.validate()
        self.assertIn("sample_rate must be between 0.0 and 1.0", str(context.exception))


if __name__ == "__main__":
    unittest.main()
