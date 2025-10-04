#!/usr/bin/env python3
"""
Example usage of the RIMP telemetry system.

This script demonstrates how to create projects and emit real-time telemetry events.
"""

from telemetry import Project, ProjectType, Priority, Area, TelemetryEvent, EventEmitter
from telemetry.events import EventType


def main():
    """Main example function."""
    print("=" * 60)
    print("RIMP Telemetry System - Example Usage")
    print("=" * 60)
    print()
    
    # Create a project with the exact specifications from the issue
    print("Creating a project: 'Bootstrap telemetría'")
    project = Project(
        title="Bootstrap telemetría",
        type=ProjectType.FEATURE,
        priority=Priority.P1,
        area=Area.REALTIME,
        sprint="Current",
        estimate=3
    )
    
    print(f"  Title: {project.title}")
    print(f"  Type: {project.type.value}")
    print(f"  Priority: {project.priority.value}")
    print(f"  Area: {project.area.value}")
    print(f"  Sprint: {project.sprint}")
    print(f"  Estimate: {project.estimate} points")
    print(f"  Created at: {project.created_at}")
    print()
    
    # Initialize event emitter for real-time telemetry
    print("Initializing real-time telemetry event system...")
    emitter = EventEmitter()
    
    # Register event listeners
    def on_project_created(event):
        data = event.data
        print(f"  [EVENT] Project created: '{data['title']}'")
        print(f"          Type: {data['type']}, Priority: {data['priority']}")
        print(f"          Area: {data['area']}, Sprint: {data['sprint']}")
        print(f"          Estimate: {data['estimate']} points")
    
    emitter.on(EventType.PROJECT_CREATED, on_project_created)
    print()
    
    # Emit project created event
    print("Emitting PROJECT_CREATED event...")
    event = TelemetryEvent(
        event_type=EventType.PROJECT_CREATED,
        data=project.to_dict()
    )
    emitter.emit(event)
    print()
    
    # Create additional example projects
    print("Creating additional projects...")
    projects = [
        Project(
            title="User Authentication",
            type=ProjectType.FEATURE,
            priority=Priority.P0,
            area=Area.BACKEND,
            sprint="Sprint 1",
            estimate=5
        ),
        Project(
            title="Fix login bug",
            type=ProjectType.BUG,
            priority=Priority.P1,
            area=Area.FRONTEND,
            sprint="Current",
            estimate=2
        ),
        Project(
            title="Infrastructure setup",
            type=ProjectType.TASK,
            priority=Priority.P2,
            area=Area.INFRASTRUCTURE,
            sprint="Sprint 2",
            estimate=8
        )
    ]
    
    for proj in projects:
        event = TelemetryEvent(
            event_type=EventType.PROJECT_CREATED,
            data=proj.to_dict()
        )
        emitter.emit(event)
    
    print()
    
    # Display telemetry statistics
    print("=" * 60)
    print("Telemetry Statistics")
    print("=" * 60)
    all_events = emitter.get_events()
    print(f"Total events captured: {len(all_events)}")
    
    project_events = emitter.get_events(EventType.PROJECT_CREATED)
    print(f"Project creation events: {len(project_events)}")
    print()
    
    print("Event timeline:")
    for i, evt in enumerate(project_events, 1):
        print(f"  {i}. {evt.data['title']} - {evt.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print()
    print("=" * 60)
    print("Telemetry system demonstration complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
