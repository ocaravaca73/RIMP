"""
Tests for telemetry collector.
"""

import unittest
import time
from telemetry.collector import TelemetryCollector
from telemetry.config import TelemetryConfig
from telemetry.models import Metric, Event, Trace, MetricType, EventSeverity


class TestTelemetryCollector(unittest.TestCase):
    """Test cases for TelemetryCollector class."""
    
    def setUp(self):
        """Set up test collector."""
        self.config = TelemetryConfig(
            enabled=True,
            buffer_size=10,
            flush_interval_ms=100,
            sample_rate=1.0
        )
        self.collector = TelemetryCollector(self.config)
        self.exported_data = []
        
    def tearDown(self):
        """Clean up test collector."""
        if self.collector._running:
            self.collector.stop()
            
    def test_collector_initialization(self):
        """Test collector initialization."""
        self.assertFalse(self.collector._running)
        self.assertEqual(self.collector.config, self.config)
        
    def test_collector_start_stop(self):
        """Test starting and stopping collector."""
        self.collector.start()
        self.assertTrue(self.collector._running)
        
        self.collector.stop()
        self.assertFalse(self.collector._running)
        
    def test_collect_metric(self):
        """Test collecting a metric."""
        def test_exporter(data_type, data):
            self.exported_data.append((data_type, data))
            
        self.collector.register_exporter(test_exporter)
        self.collector.start()
        
        metric = Metric(name="test_metric", value=100.0)
        self.collector.collect_metric(metric)
        
        # Wait for flush
        time.sleep(0.2)
        self.collector.stop()
        
        self.assertEqual(len(self.exported_data), 1)
        self.assertEqual(self.exported_data[0][0], "metric")
        self.assertEqual(self.exported_data[0][1].name, "test_metric")
        
    def test_collect_event(self):
        """Test collecting an event."""
        def test_exporter(data_type, data):
            self.exported_data.append((data_type, data))
            
        self.collector.register_exporter(test_exporter)
        self.collector.start()
        
        event = Event(name="test_event", message="Test message")
        self.collector.collect_event(event)
        
        # Wait for flush
        time.sleep(0.2)
        self.collector.stop()
        
        self.assertEqual(len(self.exported_data), 1)
        self.assertEqual(self.exported_data[0][0], "event")
        self.assertEqual(self.exported_data[0][1].name, "test_event")
        
    def test_collect_trace(self):
        """Test collecting a trace."""
        def test_exporter(data_type, data):
            self.exported_data.append((data_type, data))
            
        self.collector.register_exporter(test_exporter)
        self.collector.start()
        
        trace = Trace(
            trace_id="trace-123",
            span_id="span-001",
            operation="test_operation"
        )
        self.collector.collect_trace(trace)
        
        # Wait for flush
        time.sleep(0.2)
        self.collector.stop()
        
        self.assertEqual(len(self.exported_data), 1)
        self.assertEqual(self.exported_data[0][0], "trace")
        self.assertEqual(self.exported_data[0][1].trace_id, "trace-123")
        
    def test_disabled_collector(self):
        """Test that disabled collector doesn't collect data."""
        config = TelemetryConfig(enabled=False)
        collector = TelemetryCollector(config)
        
        def test_exporter(data_type, data):
            self.exported_data.append((data_type, data))
            
        collector.register_exporter(test_exporter)
        collector.start()
        
        metric = Metric(name="test_metric", value=100.0)
        collector.collect_metric(metric)
        
        time.sleep(0.2)
        collector.stop()
        
        self.assertEqual(len(self.exported_data), 0)
        
    def test_global_tags(self):
        """Test that global tags are applied to telemetry."""
        config = TelemetryConfig(tags={"env": "test", "version": "1.0"})
        collector = TelemetryCollector(config)
        
        def test_exporter(data_type, data):
            self.exported_data.append((data_type, data))
            
        collector.register_exporter(test_exporter)
        collector.start()
        
        metric = Metric(name="test_metric", value=100.0)
        collector.collect_metric(metric)
        
        time.sleep(0.2)
        collector.stop()
        
        self.assertEqual(len(self.exported_data), 1)
        exported_metric = self.exported_data[0][1]
        self.assertIn("env", exported_metric.tags)
        self.assertEqual(exported_metric.tags["env"], "test")
        self.assertIn("version", exported_metric.tags)
        self.assertEqual(exported_metric.tags["version"], "1.0")


if __name__ == "__main__":
    unittest.main()
