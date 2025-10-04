"""
Example usage of the telemetry system.

This script demonstrates how to use the telemetry collector to capture
metrics, events, and traces in real-time.
"""

import time
import json
from telemetry import TelemetryCollector, Metric, Event, Trace, TelemetryConfig
from telemetry.models import MetricType, EventSeverity


def console_exporter(data_type: str, data):
    """Simple exporter that prints telemetry data to console."""
    print(f"[{data_type.upper()}] {json.dumps(data.to_dict(), indent=2)}")


def main():
    """Run telemetry example."""
    print("=== Real-time Telemetry Bootstrap Example ===\n")
    
    # Configure telemetry
    config = TelemetryConfig(
        enabled=True,
        buffer_size=100,
        flush_interval_ms=2000,  # Flush every 2 seconds
        sample_rate=1.0,  # Capture 100% of telemetry
        tags={"environment": "demo", "version": "0.1.0"}
    )
    
    # Create and start collector
    collector = TelemetryCollector(config)
    collector.register_exporter(console_exporter)
    collector.start()
    
    print("Telemetry collector started. Collecting data...\n")
    
    # Simulate collecting metrics
    print("1. Collecting metrics...")
    for i in range(3):
        metric = Metric(
            name="cpu_usage",
            value=45.5 + i * 5,
            metric_type=MetricType.GAUGE,
            tags={"host": "server-01", "core": str(i)}
        )
        collector.collect_metric(metric)
    
    # Simulate collecting events
    print("2. Collecting events...")
    collector.collect_event(Event(
        name="user_login",
        message="User logged in successfully",
        severity=EventSeverity.INFO,
        metadata={"user_id": "12345", "ip": "192.168.1.1"}
    ))
    
    collector.collect_event(Event(
        name="api_error",
        message="Failed to connect to database",
        severity=EventSeverity.ERROR,
        metadata={"endpoint": "/api/users", "error_code": "DB_TIMEOUT"}
    ))
    
    # Simulate collecting traces
    print("3. Collecting traces...")
    collector.collect_trace(Trace(
        trace_id="trace-123",
        span_id="span-001",
        operation="api_request",
        duration_ms=125.5,
        tags={"method": "GET", "path": "/api/data"}
    ))
    
    collector.collect_trace(Trace(
        trace_id="trace-123",
        span_id="span-002",
        operation="database_query",
        duration_ms=85.3,
        parent_span_id="span-001",
        tags={"query": "SELECT * FROM users"}
    ))
    
    # Wait for flush
    print("\nWaiting for telemetry to be flushed...\n")
    time.sleep(3)
    
    # Stop collector
    collector.stop()
    print("\nTelemetry collector stopped.")


if __name__ == "__main__":
    main()
