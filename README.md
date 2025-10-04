# RIMP - Real-Time Telemetry System

A lightweight, modular real-time telemetry system for collecting, processing, and streaming events and metrics.

## Features

- **Event Collection**: Capture events with timestamps, severity levels, and metadata
- **Metric Tracking**: Record various metric types (counters, gauges, histograms, timers)
- **Real-Time Streaming**: Stream telemetry data to consumers in real-time
- **Configurable**: Flexible configuration via files, dictionaries, or environment variables
- **Thread-Safe**: Safe for concurrent use in multi-threaded applications
- **Extensible**: Easy to extend with custom handlers and processors

## Installation

```bash
# Clone the repository
git clone https://github.com/ocaravaca73/RIMP.git
cd RIMP

# The telemetry module is ready to use (Python 3.7+ required)
```

## Quick Start

### Basic Event and Metric Collection

```python
from telemetry import TelemetryCollector
from telemetry.models import TelemetryLevel, MetricType

# Create a collector
collector = TelemetryCollector(source="my-service")

# Collect an event
collector.collect_event(
    event_type="application.start",
    message="Application started",
    level=TelemetryLevel.INFO,
)

# Collect a metric
collector.collect_metric(
    name="cpu.usage",
    value=45.2,
    metric_type=MetricType.GAUGE,
    unit="percent",
)

# Retrieve collected data
events = collector.get_events()
metrics = collector.get_metrics()
```

### Real-Time Streaming

```python
from telemetry import TelemetryCollector, TelemetryStream

# Create collector and stream
collector = TelemetryCollector(source="streaming-service")
stream = TelemetryStream(buffer_size=1000)

# Connect collector to stream
collector.on_event(stream.push_event)
collector.on_metric(stream.push_metric)

# Subscribe to receive telemetry data
def handle_telemetry(item):
    print(f"Received: {item}")

stream.subscribe(handle_telemetry)

# Start streaming
stream.start()

# Collect telemetry - it will be streamed in real-time
collector.collect_event("user.action", "User logged in")

# Stop when done
stream.stop()
```

### Configuration

```python
from telemetry.config import TelemetryConfig

# From dictionary
config = TelemetryConfig.from_dict({
    "enabled": True,
    "source": "my-service",
    "buffer_size": 1000,
})

# From environment variables
config = TelemetryConfig.from_env()

# From file
config = TelemetryConfig.from_file("telemetry_config.json")
```

## Architecture

The telemetry system consists of four main components:

1. **Models** (`telemetry/models.py`): Data structures for events and metrics
2. **Collector** (`telemetry/collector.py`): Central collection point for telemetry data
3. **Stream** (`telemetry/stream.py`): Real-time streaming infrastructure
4. **Config** (`telemetry/config.py`): Configuration management

## Examples

See the `examples/telemetry_example.py` file for comprehensive usage examples:

```bash
python examples/telemetry_example.py
```

## Telemetry Data Models

### TelemetryEvent

Events represent discrete occurrences in the system:
- `timestamp`: When the event occurred
- `source`: Origin of the event
- `event_type`: Category/type of event
- `level`: Severity (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `message`: Human-readable description
- `metadata`: Additional contextual information

### TelemetryMetric

Metrics represent measurements over time:
- `timestamp`: When the metric was recorded
- `name`: Name of the metric
- `value`: Numeric value
- `metric_type`: Type (COUNTER, GAUGE, HISTOGRAM, TIMER)
- `unit`: Unit of measurement (optional)
- `tags`: Dimension tags for filtering/grouping

## Use Cases

- **Application Monitoring**: Track application health and performance
- **User Activity**: Monitor user interactions and behaviors
- **System Metrics**: Collect CPU, memory, network statistics
- **Business Analytics**: Track business KPIs in real-time
- **Debugging**: Capture detailed diagnostic information
- **Alerting**: Trigger alerts based on telemetry data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
