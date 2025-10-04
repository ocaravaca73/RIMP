"""
Unit tests for the telemetry system.
"""

import unittest
import time
from datetime import datetime
from telemetry import TelemetryCollector, TelemetryStream
from telemetry.models import TelemetryEvent, TelemetryMetric, TelemetryLevel, MetricType
from telemetry.config import TelemetryConfig


class TestTelemetryModels(unittest.TestCase):
    """Test telemetry data models."""
    
    def test_telemetry_event_creation(self):
        """Test creating a TelemetryEvent."""
        event = TelemetryEvent(
            timestamp=datetime.now(),
            source="test",
            event_type="test.event",
            level=TelemetryLevel.INFO,
            message="Test message",
            metadata={"key": "value"},
        )
        
        self.assertEqual(event.source, "test")
        self.assertEqual(event.event_type, "test.event")
        self.assertEqual(event.level, TelemetryLevel.INFO)
        self.assertEqual(event.message, "Test message")
        self.assertEqual(event.metadata["key"], "value")
    
    def test_telemetry_event_to_dict(self):
        """Test converting TelemetryEvent to dictionary."""
        event = TelemetryEvent(
            timestamp=datetime.now(),
            source="test",
            event_type="test.event",
        )
        
        event_dict = event.to_dict()
        
        self.assertIn("timestamp", event_dict)
        self.assertEqual(event_dict["source"], "test")
        self.assertEqual(event_dict["event_type"], "test.event")
    
    def test_telemetry_metric_creation(self):
        """Test creating a TelemetryMetric."""
        metric = TelemetryMetric(
            timestamp=datetime.now(),
            name="cpu.usage",
            value=45.2,
            metric_type=MetricType.GAUGE,
            unit="percent",
            tags={"host": "server01"},
        )
        
        self.assertEqual(metric.name, "cpu.usage")
        self.assertEqual(metric.value, 45.2)
        self.assertEqual(metric.metric_type, MetricType.GAUGE)
        self.assertEqual(metric.unit, "percent")
        self.assertEqual(metric.tags["host"], "server01")
    
    def test_telemetry_metric_to_dict(self):
        """Test converting TelemetryMetric to dictionary."""
        metric = TelemetryMetric(
            timestamp=datetime.now(),
            name="cpu.usage",
            value=45.2,
        )
        
        metric_dict = metric.to_dict()
        
        self.assertIn("timestamp", metric_dict)
        self.assertEqual(metric_dict["name"], "cpu.usage")
        self.assertEqual(metric_dict["value"], 45.2)


class TestTelemetryCollector(unittest.TestCase):
    """Test telemetry collector."""
    
    def setUp(self):
        """Set up test collector."""
        self.collector = TelemetryCollector(source="test-service")
    
    def test_collect_event(self):
        """Test collecting an event."""
        event = self.collector.collect_event(
            event_type="test.event",
            message="Test message",
        )
        
        self.assertIsInstance(event, TelemetryEvent)
        self.assertEqual(event.event_type, "test.event")
        self.assertEqual(event.message, "Test message")
        self.assertEqual(event.source, "test-service")
    
    def test_collect_metric(self):
        """Test collecting a metric."""
        metric = self.collector.collect_metric(
            name="test.metric",
            value=100.0,
        )
        
        self.assertIsInstance(metric, TelemetryMetric)
        self.assertEqual(metric.name, "test.metric")
        self.assertEqual(metric.value, 100.0)
    
    def test_get_events(self):
        """Test retrieving events."""
        self.collector.collect_event("event1", "Message 1")
        self.collector.collect_event("event2", "Message 2")
        
        events = self.collector.get_events()
        
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0].event_type, "event1")
        self.assertEqual(events[1].event_type, "event2")
    
    def test_get_metrics(self):
        """Test retrieving metrics."""
        self.collector.collect_metric("metric1", 10.0)
        self.collector.collect_metric("metric2", 20.0)
        
        metrics = self.collector.get_metrics()
        
        self.assertEqual(len(metrics), 2)
        self.assertEqual(metrics[0].name, "metric1")
        self.assertEqual(metrics[1].name, "metric2")
    
    def test_get_events_with_limit(self):
        """Test retrieving events with limit."""
        for i in range(5):
            self.collector.collect_event(f"event{i}", f"Message {i}")
        
        events = self.collector.get_events(limit=3)
        
        self.assertEqual(len(events), 3)
        self.assertEqual(events[0].event_type, "event2")
    
    def test_clear(self):
        """Test clearing collected data."""
        self.collector.collect_event("event1", "Message 1")
        self.collector.collect_metric("metric1", 10.0)
        
        self.collector.clear()
        
        self.assertEqual(len(self.collector.get_events()), 0)
        self.assertEqual(len(self.collector.get_metrics()), 0)
    
    def test_event_handler(self):
        """Test event handler callback."""
        received_events = []
        
        def handler(event):
            received_events.append(event)
        
        self.collector.on_event(handler)
        self.collector.collect_event("test.event", "Test message")
        
        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0].event_type, "test.event")


class TestTelemetryStream(unittest.TestCase):
    """Test telemetry streaming."""
    
    def setUp(self):
        """Set up test stream."""
        self.stream = TelemetryStream(buffer_size=100)
    
    def tearDown(self):
        """Clean up stream."""
        if self.stream._running:
            self.stream.stop()
    
    def test_push_event(self):
        """Test pushing an event to the stream."""
        event = TelemetryEvent(
            timestamp=datetime.now(),
            source="test",
            event_type="test.event",
        )
        
        self.stream.push_event(event)
        
        self.assertGreater(self.stream._event_queue.qsize(), 0)
    
    def test_push_metric(self):
        """Test pushing a metric to the stream."""
        metric = TelemetryMetric(
            timestamp=datetime.now(),
            name="test.metric",
            value=100.0,
        )
        
        self.stream.push_metric(metric)
        
        self.assertGreater(self.stream._metric_queue.qsize(), 0)
    
    def test_subscribe(self):
        """Test subscribing to the stream."""
        received_items = []
        
        def handler(item):
            received_items.append(item)
        
        self.stream.subscribe(handler)
        self.stream.start()
        
        event = TelemetryEvent(
            timestamp=datetime.now(),
            source="test",
            event_type="test.event",
        )
        self.stream.push_event(event)
        
        time.sleep(0.5)
        self.stream.stop()
        
        self.assertEqual(len(received_items), 1)
    
    def test_start_stop(self):
        """Test starting and stopping the stream."""
        self.stream.start()
        self.assertTrue(self.stream._running)
        
        self.stream.stop()
        self.assertFalse(self.stream._running)


class TestTelemetryConfig(unittest.TestCase):
    """Test telemetry configuration."""
    
    def test_default_config(self):
        """Test creating default configuration."""
        config = TelemetryConfig()
        
        self.assertTrue(config.enabled)
        self.assertEqual(config.source, "rimp")
        self.assertEqual(config.buffer_size, 1000)
    
    def test_config_from_dict(self):
        """Test creating configuration from dictionary."""
        config = TelemetryConfig.from_dict({
            "enabled": False,
            "source": "custom",
            "buffer_size": 500,
        })
        
        self.assertFalse(config.enabled)
        self.assertEqual(config.source, "custom")
        self.assertEqual(config.buffer_size, 500)
    
    def test_config_to_dict(self):
        """Test converting configuration to dictionary."""
        config = TelemetryConfig(
            enabled=True,
            source="test",
            buffer_size=200,
        )
        
        config_dict = config.to_dict()
        
        self.assertEqual(config_dict["enabled"], True)
        self.assertEqual(config_dict["source"], "test")
        self.assertEqual(config_dict["buffer_size"], 200)


if __name__ == "__main__":
    unittest.main()
