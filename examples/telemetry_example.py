"""
Example usage of the RIMP Real-Time Telemetry System.

This example demonstrates the basic usage of the telemetry system
including event collection, metric tracking, and real-time streaming.
"""

from datetime import datetime
import time
from telemetry import TelemetryCollector, TelemetryStream, TelemetryEvent, TelemetryMetric
from telemetry.models import TelemetryLevel, MetricType
from telemetry.config import TelemetryConfig


def print_telemetry_item(item):
    """Print telemetry items as they arrive."""
    if isinstance(item, TelemetryEvent):
        print(f"[EVENT] {item.timestamp.isoformat()} - {item.source} - {item.event_type}: {item.message}")
    elif isinstance(item, TelemetryMetric):
        print(f"[METRIC] {item.timestamp.isoformat()} - {item.name}: {item.value} {item.unit or ''}")


def example_basic_usage():
    """Demonstrate basic telemetry collection."""
    print("=== Basic Telemetry Collection ===\n")
    
    # Create a collector
    collector = TelemetryCollector(source="example-service")
    
    # Collect some events
    collector.collect_event(
        event_type="application.start",
        message="Application started successfully",
        level=TelemetryLevel.INFO,
    )
    
    collector.collect_event(
        event_type="user.action",
        message="User performed action",
        level=TelemetryLevel.INFO,
        user_id="user123",
        action="login",
    )
    
    # Collect some metrics
    collector.collect_metric(
        name="cpu.usage",
        value=45.2,
        metric_type=MetricType.GAUGE,
        unit="percent",
        host="server01",
    )
    
    collector.collect_metric(
        name="requests.total",
        value=1523,
        metric_type=MetricType.COUNTER,
        endpoint="/api/users",
    )
    
    # Retrieve collected data
    events = collector.get_events()
    metrics = collector.get_metrics()
    
    print(f"Collected {len(events)} events and {len(metrics)} metrics\n")
    
    for event in events:
        print(f"Event: {event.event_type} - {event.message}")
    
    for metric in metrics:
        print(f"Metric: {metric.name} = {metric.value} {metric.unit or ''}")


def example_realtime_streaming():
    """Demonstrate real-time telemetry streaming."""
    print("\n\n=== Real-Time Telemetry Streaming ===\n")
    
    # Create collector and stream
    collector = TelemetryCollector(source="streaming-service")
    stream = TelemetryStream(buffer_size=100)
    
    # Connect collector to stream
    collector.on_event(stream.push_event)
    collector.on_metric(stream.push_metric)
    
    # Subscribe to stream
    stream.subscribe(print_telemetry_item)
    
    # Start streaming
    stream.start()
    
    # Simulate telemetry generation
    print("Generating telemetry data...\n")
    for i in range(5):
        collector.collect_event(
            event_type="process.step",
            message=f"Processing step {i+1}",
            step_number=i+1,
        )
        
        collector.collect_metric(
            name="process.duration",
            value=0.5 + (i * 0.1),
            metric_type=MetricType.TIMER,
            unit="seconds",
        )
        
        time.sleep(0.5)
    
    # Give stream time to process
    time.sleep(1)
    
    # Stop streaming
    stream.stop()
    
    pending = stream.get_pending_count()
    print(f"\nStream stopped. Pending items: {pending}")


def example_with_configuration():
    """Demonstrate configuration usage."""
    print("\n\n=== Configuration Example ===\n")
    
    # Create configuration
    config = TelemetryConfig(
        enabled=True,
        source="configured-service",
        buffer_size=500,
        retention_limit=5000,
    )
    
    print(f"Configuration:")
    print(f"  Enabled: {config.enabled}")
    print(f"  Source: {config.source}")
    print(f"  Buffer Size: {config.buffer_size}")
    print(f"  Retention Limit: {config.retention_limit}")
    
    # Use configuration
    if config.enabled:
        collector = TelemetryCollector(source=config.source)
        collector.collect_event(
            event_type="config.loaded",
            message="Configuration loaded successfully",
        )
        
        print(f"\nCollected {len(collector.get_events())} events")


if __name__ == "__main__":
    # Run examples
    example_basic_usage()
    example_realtime_streaming()
    example_with_configuration()
    
    print("\n\n=== Examples Complete ===")
