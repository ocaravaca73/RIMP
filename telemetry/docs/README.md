# Real-time Telemetry System - ISBL

## Overview

This is the bootstrap implementation of a real-time telemetry infrastructure for the RIMP project. It provides a foundation for collecting, buffering, and processing telemetry events in real-time.

## Architecture

The telemetry system consists of three main components:

### 1. TelemetryEvent
Represents a single telemetry event with the following attributes:
- `event_id`: Unique identifier (UUID)
- `timestamp`: Event timestamp (UTC)
- `event_type`: Category of the event
- `source`: Source system or component
- `data`: Event payload (flexible dictionary)
- `metadata`: Additional metadata

### 2. DataCollector
Handles collection and buffering of telemetry events:
- Thread-safe event collection
- Configurable buffer size
- Batch retrieval of events
- Callback support for real-time processing
- Statistics tracking

### 3. TelemetryService
High-level service interface:
- Configuration management
- Service lifecycle (start/stop)
- Event emission
- Event retrieval
- Statistics and monitoring

## Usage

### Basic Example

```python
from telemetry.core import TelemetryService
from telemetry.config import load_config

# Initialize service
config = load_config()
telemetry = TelemetryService(config)

# Start collecting
telemetry.start()

# Emit events
telemetry.emit(
    event_type='user.action',
    source='my-app',
    data={'action': 'login', 'user_id': '123'}
)

# Retrieve events
events = telemetry.get_events(batch_size=10)

# Get statistics
stats = telemetry.get_stats()

# Stop service
telemetry.stop()
```

### Configuration

Default configuration options:
- `enabled`: Enable/disable telemetry (default: `True`)
- `buffer_size`: Maximum events to buffer (default: `1000`)
- `batch_size`: Events per batch (default: `10`)
- `source_id`: Instance identifier (default: `'isbl-telemetry'`)
- `event_types`: Filter by event types (default: all)
- `sampling_rate`: Event sampling rate (default: `1.0`)

## Running Examples

```bash
cd /home/runner/work/RIMP/RIMP
python -m telemetry.examples.basic_usage
```

## Event Types

Common event type categories:
- `system.*`: System-level events (startup, shutdown, errors)
- `user.*`: User actions and interactions
- `metric.*`: Performance and resource metrics
- `data.*`: Data processing events
- `alert.*`: Alerts and notifications

## Future Enhancements

- Persistent storage backend
- Network streaming support
- Advanced filtering and aggregation
- Dashboard and visualization
- Integration with monitoring systems
