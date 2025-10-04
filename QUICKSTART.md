# RIMP Telemetry System - Quick Reference

## Installation

No dependencies required - uses only Python standard library (Python 3.7+)

## Basic Usage

### 1. Import Components

```python
from telemetry import TelemetryCollector, TelemetryStream
from telemetry.models import TelemetryLevel, MetricType
from telemetry.config import TelemetryConfig
```

### 2. Create a Collector

```python
collector = TelemetryCollector(source="my-service")
```

### 3. Collect Events

```python
# Simple event
collector.collect_event(
    event_type="app.started",
    message="Application started"
)

# Event with metadata
collector.collect_event(
    event_type="user.login",
    message="User logged in",
    level=TelemetryLevel.INFO,
    user_id="user123",
    ip_address="192.168.1.1"
)
```

### 4. Collect Metrics

```python
# Gauge metric
collector.collect_metric(
    name="cpu.usage",
    value=45.2,
    metric_type=MetricType.GAUGE,
    unit="percent"
)

# Counter metric with tags
collector.collect_metric(
    name="requests.total",
    value=1000,
    metric_type=MetricType.COUNTER,
    endpoint="/api/users",
    method="GET"
)
```

### 5. Retrieve Data

```python
# Get all events
events = collector.get_events()

# Get last 10 events
recent_events = collector.get_events(limit=10)

# Get all metrics
metrics = collector.get_metrics()
```

### 6. Real-Time Streaming

```python
# Create stream
stream = TelemetryStream(buffer_size=1000)

# Connect collector to stream
collector.on_event(stream.push_event)
collector.on_metric(stream.push_metric)

# Subscribe to stream
def handle_telemetry(item):
    print(f"Received: {item}")

stream.subscribe(handle_telemetry)

# Start streaming
stream.start()

# ... collect telemetry ...

# Stop streaming
stream.stop()
```

## Configuration

### From Dictionary

```python
config = TelemetryConfig.from_dict({
    "enabled": True,
    "source": "my-service",
    "buffer_size": 1000,
    "retention_limit": 10000
})
```

### From File

```python
config = TelemetryConfig.from_file("telemetry_config.json")
```

### From Environment Variables

```bash
export TELEMETRY_ENABLED=true
export TELEMETRY_SOURCE=my-service
export TELEMETRY_BUFFER_SIZE=1000
```

```python
config = TelemetryConfig.from_env()
```

## Event Levels

- `TelemetryLevel.DEBUG` - Detailed debug information
- `TelemetryLevel.INFO` - General informational messages
- `TelemetryLevel.WARNING` - Warning messages
- `TelemetryLevel.ERROR` - Error messages
- `TelemetryLevel.CRITICAL` - Critical failure messages

## Metric Types

- `MetricType.COUNTER` - Monotonically increasing counter
- `MetricType.GAUGE` - Point-in-time value that can go up or down
- `MetricType.HISTOGRAM` - Distribution of values
- `MetricType.TIMER` - Duration/timing measurements

## Common Patterns

### Application Monitoring

```python
collector = TelemetryCollector(source="app")

# Startup
collector.collect_event("app.started", "Application started")

# Health check
collector.collect_metric("health.status", 1.0, MetricType.GAUGE)
```

### Request Tracking

```python
# Request received
collector.collect_event(
    "request.received",
    "HTTP request received",
    method="GET",
    path="/api/users",
    request_id="req-123"
)

# Request duration
collector.collect_metric(
    "request.duration",
    0.245,
    MetricType.TIMER,
    unit="seconds",
    endpoint="/api/users"
)
```

### Error Handling

```python
try:
    # ... some operation ...
    pass
except Exception as e:
    collector.collect_event(
        "error.occurred",
        f"Error: {str(e)}",
        level=TelemetryLevel.ERROR,
        error_type=type(e).__name__,
        stack_trace=traceback.format_exc()
    )
```

## Running Tests

```bash
cd /path/to/RIMP
PYTHONPATH=/path/to/RIMP python -m unittest tests.test_telemetry
```

## Running Examples

```bash
cd /path/to/RIMP
PYTHONPATH=/path/to/RIMP python examples/telemetry_example.py
```

## Architecture

```
telemetry/
├── __init__.py       # Package exports
├── models.py         # TelemetryEvent, TelemetryMetric data classes
├── collector.py      # TelemetryCollector for gathering data
├── stream.py         # TelemetryStream for real-time processing
└── config.py         # TelemetryConfig for configuration
```

## Thread Safety

All components are thread-safe:
- Collector uses locks for concurrent access
- Stream uses thread-safe queues
- Multiple threads can collect telemetry simultaneously

## Performance Considerations

- Events and metrics are stored in memory (configure `retention_limit`)
- Stream uses bounded queues (configure `buffer_size`)
- Old items are dropped when buffers are full
- Subscriber errors don't break the stream
