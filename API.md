# RIMP Telemetry API Documentation

## Overview

The RIMP Telemetry System provides real-time collection, processing, and storage of application metrics and events.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Core Components](#core-components)
3. [Configuration](#configuration)
4. [Data Models](#data-models)
5. [Collector API](#collector-api)
6. [Storage API](#storage-api)
7. [Streaming API](#streaming-api)
8. [Best Practices](#best-practices)

## Quick Start

```python
from telemetry import TelemetryCollector, TelemetryConfig, EventType

# Create and configure collector
config = TelemetryConfig(enabled=True, realtime_mode=True)
collector = TelemetryCollector(config)

# Collect an event
collector.collect_event(
    source="my_app",
    message="User logged in",
    event_type=EventType.INFO,
    metadata={"user_id": "123"}
)

# Collect a metric
collector.collect_metric(
    name="response_time",
    value=125.5,
    unit="ms",
    tags={"endpoint": "/api/users"}
)
```

## Core Components

### TelemetryCollector

Thread-safe collector for events and metrics with automatic buffering.

**Key Features:**
- Automatic buffering with configurable size
- Real-time listener support
- Thread-safe operations
- Automatic flushing

### TelemetryStream

Real-time streaming of telemetry data to consumers.

**Key Features:**
- Consumer/producer pattern
- Configurable streaming intervals
- Automatic storage integration
- Background processing thread

### Storage Backends

#### MemoryStorage
In-memory storage for fast access and testing.

#### FileStorage
Persistent storage in JSONL format.

## Configuration

### TelemetryConfig

```python
from telemetry import TelemetryConfig

config = TelemetryConfig(
    enabled=True,              # Enable/disable telemetry
    buffer_size=100,           # Buffer size before auto-flush
    flush_interval=5.0,        # Auto-flush interval (seconds)
    realtime_mode=True,        # Enable real-time listeners
    storage_backend="memory",  # Backend type
    storage_path=None          # Path for file storage
)

# Validate configuration
config.validate()
```

**Parameters:**
- `enabled` (bool): Enable or disable telemetry collection
- `buffer_size` (int): Maximum items in buffer before automatic flush
- `flush_interval` (float): Seconds between automatic flushes
- `realtime_mode` (bool): Enable real-time listener notifications
- `storage_backend` (str): Storage type: "memory", "file", or "database"
- `storage_path` (str, optional): File path for file-based storage

## Data Models

### TelemetryEvent

Represents an application event.

```python
from telemetry import TelemetryEvent, EventType
from datetime import datetime

event = TelemetryEvent(
    event_id="unique-id",
    timestamp=datetime.utcnow(),
    event_type=EventType.INFO,
    source="app_name",
    message="Something happened",
    metadata={"key": "value"}
)
```

**Attributes:**
- `event_id` (str): Unique identifier
- `timestamp` (datetime): Event timestamp
- `event_type` (EventType): INFO, WARNING, ERROR, or DEBUG
- `source` (str): Event source/component
- `message` (str): Event description
- `metadata` (dict, optional): Additional data

### TelemetryMetric

Represents a numeric measurement.

```python
from telemetry import TelemetryMetric

metric = TelemetryMetric(
    metric_id="unique-id",
    timestamp=datetime.utcnow(),
    name="cpu_usage",
    value=45.2,
    unit="percent",
    tags={"host": "server-01"}
)
```

**Attributes:**
- `metric_id` (str): Unique identifier
- `timestamp` (datetime): Measurement timestamp
- `name` (str): Metric name
- `value` (float): Measured value
- `unit` (str, optional): Unit of measurement
- `tags` (dict, optional): Tags for filtering/grouping

### EventType Enum

```python
from telemetry import EventType

EventType.INFO     # Informational events
EventType.WARNING  # Warning events
EventType.ERROR    # Error events
EventType.DEBUG    # Debug events
```

## Collector API

### collect_event()

Collect a telemetry event.

```python
event = collector.collect_event(
    source="component_name",
    message="Event description",
    event_type=EventType.INFO,
    metadata={"additional": "data"}
)
```

**Parameters:**
- `source` (str): Event source
- `message` (str): Event message
- `event_type` (EventType): Event severity level
- `metadata` (dict, optional): Additional metadata

**Returns:** `TelemetryEvent` or None if disabled

### collect_metric()

Collect a telemetry metric.

```python
metric = collector.collect_metric(
    name="metric_name",
    value=123.45,
    unit="units",
    tags={"tag1": "value1"}
)
```

**Parameters:**
- `name` (str): Metric name
- `value` (float): Metric value
- `unit` (str, optional): Unit of measurement
- `tags` (dict, optional): Metric tags

**Returns:** `TelemetryMetric` or None if disabled

### add_listener()

Add a real-time listener for telemetry data.

```python
def my_listener(data):
    print(f"Received {len(data.events)} events")

collector.add_listener(my_listener)
```

**Parameters:**
- `listener` (Callable): Function receiving TelemetryData

### flush()

Manually flush the buffer.

```python
data = collector.flush()
print(f"Flushed {len(data.events)} events")
```

**Returns:** `TelemetryData` containing flushed items

## Storage API

### MemoryStorage

In-memory storage implementation.

```python
from telemetry.storage import MemoryStorage

storage = MemoryStorage()

# Store data
storage.store(telemetry_data)

# Retrieve data
data = storage.retrieve(limit=100)

# Clear storage
storage.clear()
```

### FileStorage

File-based persistent storage.

```python
from telemetry.storage import FileStorage

storage = FileStorage("/path/to/telemetry.jsonl")

# Store data (appends to file)
storage.store(telemetry_data)

# Retrieve data
data = storage.retrieve(limit=100)
```

### retrieve()

Retrieve stored telemetry data.

```python
data = storage.retrieve(
    start_time=datetime(2025, 1, 1),
    end_time=datetime(2025, 12, 31),
    limit=1000
)
```

**Parameters:**
- `start_time` (datetime, optional): Start of time range
- `end_time` (datetime, optional): End of time range
- `limit` (int, optional): Maximum items to retrieve

**Returns:** `TelemetryData`

## Streaming API

### TelemetryStream

Real-time streaming of telemetry data.

```python
from telemetry.streaming import TelemetryStream
from telemetry.storage import MemoryStorage

stream = TelemetryStream(
    collector=collector,
    storage=storage,
    interval=1.0  # seconds
)
```

### add_consumer()

Add a consumer for streamed data.

```python
def process_data(data):
    for event in data.events:
        print(f"Event: {event.message}")
    for metric in data.metrics:
        print(f"Metric: {metric.name} = {metric.value}")

stream.add_consumer(process_data)
```

### start() / stop()

Control stream lifecycle.

```python
# Start streaming
stream.start()

# ... application runs ...

# Stop streaming
stream.stop()
```

## Best Practices

### 1. Use Context-Appropriate Event Types

```python
# Good
collector.collect_event("auth", "Login successful", EventType.INFO)
collector.collect_event("auth", "Invalid password", EventType.WARNING)
collector.collect_event("db", "Connection failed", EventType.ERROR)

# Avoid
collector.collect_event("app", "Everything", EventType.INFO)
```

### 2. Add Meaningful Metadata

```python
# Good
collector.collect_event(
    "api",
    "Request processed",
    EventType.INFO,
    metadata={
        "endpoint": "/api/users",
        "method": "GET",
        "duration_ms": 125,
        "status_code": 200
    }
)

# Less useful
collector.collect_event("api", "Request", EventType.INFO)
```

### 3. Use Consistent Metric Names and Tags

```python
# Good - consistent naming
collector.collect_metric("http_request_duration", 125, "ms", 
                        {"endpoint": "/api/users", "method": "GET"})
collector.collect_metric("http_request_duration", 89, "ms",
                        {"endpoint": "/api/posts", "method": "POST"})

# Avoid - inconsistent
collector.collect_metric("request_time_1", 125, "ms")
collector.collect_metric("post_duration", 89, "milliseconds")
```

### 4. Configure Buffer Size Appropriately

```python
# High-volume applications
config = TelemetryConfig(buffer_size=500, flush_interval=10.0)

# Low-volume or testing
config = TelemetryConfig(buffer_size=10, flush_interval=1.0)
```

### 5. Use Storage for Persistence

```python
# Development/Testing
storage = MemoryStorage()

# Production
storage = FileStorage("/var/log/telemetry/data.jsonl")
```

### 6. Clean Up Resources

```python
try:
    stream.start()
    # ... application logic ...
finally:
    stream.stop()
```

### 7. Handle Consumer Errors

```python
def safe_consumer(data):
    try:
        # Process data
        process(data)
    except Exception as e:
        # Log but don't crash
        logger.error(f"Consumer error: {e}")

stream.add_consumer(safe_consumer)
```

## Error Handling

The telemetry system is designed to be resilient:

- Listener/consumer errors are caught and ignored
- Disabled collectors return None instead of raising errors
- Configuration validation provides clear error messages

```python
# Validate configuration
try:
    config.validate()
except ValueError as e:
    print(f"Invalid configuration: {e}")
```

## Performance Considerations

1. **Buffer Size**: Larger buffers reduce flush frequency but increase memory usage
2. **Real-time Mode**: Adds overhead for listener notifications
3. **Storage**: File storage is slower than memory but provides persistence
4. **Threading**: Collector operations are thread-safe with minimal contention

## Integration Examples

### Web Application

```python
from flask import Flask, request
from telemetry import TelemetryCollector, TelemetryConfig, EventType

app = Flask(__name__)
collector = TelemetryCollector(TelemetryConfig(enabled=True))

@app.before_request
def log_request():
    collector.collect_event(
        "web",
        f"Request: {request.method} {request.path}",
        EventType.INFO
    )

@app.after_request
def log_response(response):
    collector.collect_metric(
        "http_response_time",
        request.request_time,
        "ms",
        {"status": response.status_code}
    )
    return response
```

### Background Service

```python
import time
from telemetry import TelemetryCollector, TelemetryConfig

collector = TelemetryCollector(TelemetryConfig(enabled=True))

def monitoring_loop():
    while True:
        cpu = get_cpu_usage()
        memory = get_memory_usage()
        
        collector.collect_metric("cpu_usage", cpu, "percent")
        collector.collect_metric("memory_usage", memory, "MB")
        
        if cpu > 80:
            collector.collect_event(
                "monitor",
                f"High CPU: {cpu}%",
                EventType.WARNING
            )
        
        time.sleep(60)
```
