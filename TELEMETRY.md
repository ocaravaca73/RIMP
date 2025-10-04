# Real-time Telemetry Bootstrap

A lightweight, real-time telemetry system for collecting, processing, and streaming metrics, events, and traces.

## Overview

This telemetry bootstrap provides a foundation for monitoring applications in real-time. It supports:

- **Metrics**: Counters, gauges, and histograms for numerical measurements
- **Events**: Structured log events with severity levels
- **Traces**: Distributed tracing for performance monitoring

## Features

- ✅ Real-time data collection and buffering
- ✅ Configurable sampling rates
- ✅ Multiple exporter support
- ✅ Global tagging for all telemetry
- ✅ Thread-safe collection
- ✅ Automatic periodic flushing
- ✅ Type-safe data models

## Installation

```bash
# No external dependencies required - uses Python standard library only
python3 -m pip install -e .
```

## Quick Start

```python
from telemetry import TelemetryCollector, Metric, Event, Trace, TelemetryConfig
from telemetry.models import MetricType, EventSeverity

# Configure telemetry
config = TelemetryConfig(
    enabled=True,
    buffer_size=1000,
    flush_interval_ms=5000,
    sample_rate=1.0,
    tags={"environment": "production", "version": "1.0.0"}
)

# Create and start collector
collector = TelemetryCollector(config)
collector.start()

# Register an exporter (e.g., send to monitoring service)
def my_exporter(data_type, data):
    print(f"Exporting {data_type}: {data.to_dict()}")

collector.register_exporter(my_exporter)

# Collect metrics
metric = Metric(
    name="api_response_time",
    value=125.5,
    metric_type=MetricType.HISTOGRAM,
    tags={"endpoint": "/api/users", "method": "GET"}
)
collector.collect_metric(metric)

# Collect events
event = Event(
    name="user_action",
    message="User completed checkout",
    severity=EventSeverity.INFO,
    metadata={"user_id": "12345", "amount": 99.99}
)
collector.collect_event(event)

# Collect traces
trace = Trace(
    trace_id="trace-abc-123",
    span_id="span-001",
    operation="process_payment",
    duration_ms=234.5,
    tags={"payment_method": "credit_card"}
)
collector.collect_trace(trace)

# Stop collector when done
collector.stop()
```

## Configuration

The `TelemetryConfig` class supports the following options:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | bool | True | Enable/disable telemetry collection |
| `buffer_size` | int | 1000 | Maximum number of items to buffer |
| `flush_interval_ms` | int | 5000 | How often to flush data (milliseconds) |
| `export_endpoints` | List[str] | [] | List of export endpoints |
| `sample_rate` | float | 1.0 | Sampling rate (0.0 to 1.0) |
| `tags` | dict | {} | Global tags applied to all telemetry |

## Architecture

```
┌─────────────────┐
│  Application    │
│     Code        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Telemetry      │
│  Collector      │
│  - Buffer       │
│  - Sampling     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Exporters      │
│  - Console      │
│  - HTTP         │
│  - File         │
└─────────────────┘
```

## Data Models

### Metric
Represents numerical measurements over time.

```python
Metric(
    name="cpu_usage",
    value=75.5,
    metric_type=MetricType.GAUGE,  # COUNTER, GAUGE, or HISTOGRAM
    tags={"host": "server-01"}
)
```

### Event
Represents discrete events or log entries.

```python
Event(
    name="error_occurred",
    message="Database connection failed",
    severity=EventSeverity.ERROR,  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    metadata={"error_code": "DB_TIMEOUT"}
)
```

### Trace
Represents spans in distributed tracing.

```python
Trace(
    trace_id="trace-123",
    span_id="span-001",
    operation="api_call",
    duration_ms=123.45,
    parent_span_id="span-000",  # Optional, for nested spans
    tags={"method": "POST"}
)
```

## Running Tests

```bash
# Run all tests
python3 -m unittest discover tests

# Run specific test file
python3 -m unittest tests/test_models.py
python3 -m unittest tests/test_config.py
python3 -m unittest tests/test_collector.py
```

## Example

Run the included example:

```bash
python3 example.py
```

This will demonstrate collecting metrics, events, and traces with console output.

## Use Cases

1. **Application Performance Monitoring (APM)**
   - Track API response times
   - Monitor database query performance
   - Measure service dependencies

2. **System Monitoring**
   - CPU, memory, disk usage
   - Network traffic metrics
   - Process health checks

3. **Business Analytics**
   - User behavior tracking
   - Transaction monitoring
   - Feature usage metrics

4. **Debugging & Troubleshooting**
   - Distributed tracing
   - Error tracking
   - Event logging

## Future Enhancements

- HTTP exporter for remote endpoints
- File-based exporter
- Compression for large telemetry payloads
- Advanced sampling strategies
- Metric aggregation
- Integration with popular monitoring tools (Prometheus, Datadog, etc.)

## Contributing

Contributions are welcome! This is a bootstrap implementation designed to be extended.

## License

This project is open source and available under the MIT License.
