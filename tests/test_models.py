"""
Tests for telemetry models.
"""

import unittest
from datetime import datetime
from telemetry.models import Metric, Event, Trace, MetricType, EventSeverity


class TestMetric(unittest.TestCase):
    """Test cases for Metric class."""
    
    def test_metric_creation(self):
        """Test basic metric creation."""
        metric = Metric(name="test_metric", value=42.0)
        self.assertEqual(metric.name, "test_metric")
        self.assertEqual(metric.value, 42.0)
        self.assertEqual(metric.metric_type, MetricType.GAUGE)
        self.assertIsInstance(metric.timestamp, datetime)
        
    def test_metric_with_tags(self):
        """Test metric with custom tags."""
        tags = {"host": "server-01", "region": "us-east"}
        metric = Metric(name="cpu_usage", value=75.5, tags=tags)
        self.assertEqual(metric.tags, tags)
        
    def test_metric_to_dict(self):
        """Test metric serialization to dict."""
        metric = Metric(
            name="memory_usage",
            value=1024.0,
            metric_type=MetricType.GAUGE,
            tags={"unit": "MB"}
        )
        result = metric.to_dict()
        self.assertEqual(result["name"], "memory_usage")
        self.assertEqual(result["value"], 1024.0)
        self.assertEqual(result["type"], "gauge")
        self.assertIn("timestamp", result)
        self.assertEqual(result["tags"], {"unit": "MB"})


class TestEvent(unittest.TestCase):
    """Test cases for Event class."""
    
    def test_event_creation(self):
        """Test basic event creation."""
        event = Event(name="test_event", message="Test message")
        self.assertEqual(event.name, "test_event")
        self.assertEqual(event.message, "Test message")
        self.assertEqual(event.severity, EventSeverity.INFO)
        self.assertIsInstance(event.timestamp, datetime)
        
    def test_event_with_severity(self):
        """Test event with custom severity."""
        event = Event(
            name="error_event",
            message="An error occurred",
            severity=EventSeverity.ERROR
        )
        self.assertEqual(event.severity, EventSeverity.ERROR)
        
    def test_event_to_dict(self):
        """Test event serialization to dict."""
        event = Event(
            name="user_login",
            message="User logged in",
            severity=EventSeverity.INFO,
            metadata={"user_id": "123"}
        )
        result = event.to_dict()
        self.assertEqual(result["name"], "user_login")
        self.assertEqual(result["message"], "User logged in")
        self.assertEqual(result["severity"], "info")
        self.assertIn("timestamp", result)
        self.assertEqual(result["metadata"], {"user_id": "123"})


class TestTrace(unittest.TestCase):
    """Test cases for Trace class."""
    
    def test_trace_creation(self):
        """Test basic trace creation."""
        trace = Trace(
            trace_id="trace-123",
            span_id="span-001",
            operation="test_operation"
        )
        self.assertEqual(trace.trace_id, "trace-123")
        self.assertEqual(trace.span_id, "span-001")
        self.assertEqual(trace.operation, "test_operation")
        self.assertIsInstance(trace.start_time, datetime)
        self.assertIsNone(trace.duration_ms)
        self.assertIsNone(trace.parent_span_id)
        
    def test_trace_with_parent(self):
        """Test trace with parent span."""
        trace = Trace(
            trace_id="trace-123",
            span_id="span-002",
            operation="child_operation",
            parent_span_id="span-001",
            duration_ms=50.5
        )
        self.assertEqual(trace.parent_span_id, "span-001")
        self.assertEqual(trace.duration_ms, 50.5)
        
    def test_trace_to_dict(self):
        """Test trace serialization to dict."""
        trace = Trace(
            trace_id="trace-abc",
            span_id="span-xyz",
            operation="api_call",
            duration_ms=123.45,
            tags={"method": "POST"}
        )
        result = trace.to_dict()
        self.assertEqual(result["trace_id"], "trace-abc")
        self.assertEqual(result["span_id"], "span-xyz")
        self.assertEqual(result["operation"], "api_call")
        self.assertEqual(result["duration_ms"], 123.45)
        self.assertIn("start_time", result)
        self.assertEqual(result["tags"], {"method": "POST"})


if __name__ == "__main__":
    unittest.main()
