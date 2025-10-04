"""
Basic telemetry usage example
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from telemetry import TelemetryCollector, TelemetryConfig, EventType
import time


def main():
    """Demonstrate basic telemetry collection"""
    
    # Create configuration
    config = TelemetryConfig(
        enabled=True,
        buffer_size=10,
        realtime_mode=False
    )
    
    # Create collector
    collector = TelemetryCollector(config)
    
    print("Collecting telemetry events and metrics...")
    
    # Collect some events
    collector.collect_event(
        source="example_app",
        message="Application started",
        event_type=EventType.INFO
    )
    
    collector.collect_event(
        source="example_app",
        message="Processing data",
        event_type=EventType.INFO,
        metadata={"operation": "data_processing", "items": 100}
    )
    
    # Collect some metrics
    collector.collect_metric(
        name="cpu_usage",
        value=45.2,
        unit="percent",
        tags={"host": "server-01"}
    )
    
    collector.collect_metric(
        name="memory_usage",
        value=2048.5,
        unit="MB",
        tags={"host": "server-01"}
    )
    
    collector.collect_metric(
        name="request_count",
        value=150,
        unit="requests",
        tags={"endpoint": "/api/users"}
    )
    
    # Add a warning event
    collector.collect_event(
        source="example_app",
        message="High memory usage detected",
        event_type=EventType.WARNING,
        metadata={"threshold": 80, "current": 85}
    )
    
    # Check buffer size
    print(f"Current buffer size: {collector.get_buffer_size()}")
    
    # Manually flush to see collected data
    data = collector.flush()
    
    print(f"\nCollected {len(data.events)} events:")
    for event in data.events:
        print(f"  - [{event.event_type.value}] {event.source}: {event.message}")
    
    print(f"\nCollected {len(data.metrics)} metrics:")
    for metric in data.metrics:
        tags_str = f" ({metric.tags})" if metric.tags else ""
        print(f"  - {metric.name}: {metric.value} {metric.unit or ''}{tags_str}")
    
    print("\nTelemetry collection completed!")


if __name__ == "__main__":
    main()
