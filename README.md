# RIMP - Real-time Integration and Monitoring Platform

A real-time telemetry system for project task management.

## Features

- **Project Task Management**: Create and track projects with structured fields
- **Real-time Telemetry**: Event-driven system for monitoring project activities
- **Type-safe Models**: Strongly typed project fields (Type, Priority, Area, Sprint, Estimate)

## Project Fields

Projects in the telemetry system include the following fields:

- **Type**: Feature, Bug, Task, or Epic
- **Priority**: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
- **Area**: Realtime, Backend, Frontend, Infrastructure
- **Sprint**: Sprint identifier (e.g., "Current", "Sprint 1")
- **Estimate**: Story points estimate (integer)

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### Creating a Project

```python
from telemetry import Project, ProjectType, Priority, Area

project = Project(
    title="Bootstrap telemetría",
    type=ProjectType.FEATURE,
    priority=Priority.P1,
    area=Area.REALTIME,
    sprint="Current",
    estimate=3
)
```

### Using Real-time Events

```python
from telemetry import TelemetryEvent, EventEmitter
from telemetry.events import EventType

# Initialize event emitter
emitter = EventEmitter()

# Register event listener
def on_project_created(event):
    print(f"Project created: {event.data['title']}")

emitter.on(EventType.PROJECT_CREATED, on_project_created)

# Emit event
event = TelemetryEvent(
    event_type=EventType.PROJECT_CREATED,
    data=project.to_dict()
)
emitter.emit(event)
```

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_project_creation.py

# Run with unittest
python -m unittest discover tests
```

## Development

This project uses Python 3.7+ and follows standard Python development practices.

### Project Structure

```
RIMP/
├── telemetry/           # Main telemetry module
│   ├── __init__.py     # Module exports
│   ├── models.py       # Data models (Project, enums)
│   └── events.py       # Event system (TelemetryEvent, EventEmitter)
├── tests/              # Test suite
│   ├── __init__.py
│   └── test_project_creation.py
└── README.md
```

## License

MIT
