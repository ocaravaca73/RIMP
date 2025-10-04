"""
Tests for project task creation in telemetry system.
"""

import unittest
from datetime import datetime
from telemetry import Project, ProjectType, Priority, Area
from telemetry.events import TelemetryEvent, EventEmitter, EventType


class TestProjectCreation(unittest.TestCase):
    """Test cases for project task creation."""
    
    def test_create_project_with_all_fields(self):
        """Test creating a project with all required fields."""
        project = Project(
            title="Bootstrap telemetría",
            type=ProjectType.FEATURE,
            priority=Priority.P1,
            area=Area.REALTIME,
            sprint="Current",
            estimate=3
        )
        
        self.assertEqual(project.title, "Bootstrap telemetría")
        self.assertEqual(project.type, ProjectType.FEATURE)
        self.assertEqual(project.priority, Priority.P1)
        self.assertEqual(project.area, Area.REALTIME)
        self.assertEqual(project.sprint, "Current")
        self.assertEqual(project.estimate, 3)
        self.assertIsNotNone(project.created_at)
        self.assertIsInstance(project.created_at, datetime)
    
    def test_project_to_dict(self):
        """Test converting project to dictionary."""
        project = Project(
            title="Test Project",
            type=ProjectType.FEATURE,
            priority=Priority.P1,
            area=Area.REALTIME,
            sprint="Sprint 1",
            estimate=5
        )
        
        project_dict = project.to_dict()
        
        self.assertEqual(project_dict['title'], "Test Project")
        self.assertEqual(project_dict['type'], "Feature")
        self.assertEqual(project_dict['priority'], "P1")
        self.assertEqual(project_dict['area'], "Realtime")
        self.assertEqual(project_dict['sprint'], "Sprint 1")
        self.assertEqual(project_dict['estimate'], 5)
        self.assertIn('created_at', project_dict)
    
    def test_project_types(self):
        """Test different project types."""
        types = [ProjectType.FEATURE, ProjectType.BUG, ProjectType.TASK, ProjectType.EPIC]
        
        for ptype in types:
            project = Project(
                title=f"Test {ptype.value}",
                type=ptype,
                priority=Priority.P1,
                area=Area.REALTIME,
                sprint="Current",
                estimate=3
            )
            self.assertEqual(project.type, ptype)
    
    def test_project_priorities(self):
        """Test different priority levels."""
        priorities = [Priority.P0, Priority.P1, Priority.P2, Priority.P3]
        
        for priority in priorities:
            project = Project(
                title="Test Priority",
                type=ProjectType.FEATURE,
                priority=priority,
                area=Area.REALTIME,
                sprint="Current",
                estimate=3
            )
            self.assertEqual(project.priority, priority)
    
    def test_project_areas(self):
        """Test different areas."""
        areas = [Area.REALTIME, Area.BACKEND, Area.FRONTEND, Area.INFRASTRUCTURE]
        
        for area in areas:
            project = Project(
                title="Test Area",
                type=ProjectType.FEATURE,
                priority=Priority.P1,
                area=area,
                sprint="Current",
                estimate=3
            )
            self.assertEqual(project.area, area)


class TestTelemetryEvents(unittest.TestCase):
    """Test cases for telemetry event system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.emitter = EventEmitter()
    
    def test_emit_project_created_event(self):
        """Test emitting project created event."""
        project = Project(
            title="Test Project",
            type=ProjectType.FEATURE,
            priority=Priority.P1,
            area=Area.REALTIME,
            sprint="Current",
            estimate=3
        )
        
        event = TelemetryEvent(
            event_type=EventType.PROJECT_CREATED,
            data=project.to_dict()
        )
        
        self.emitter.emit(event)
        
        events = self.emitter.get_events(EventType.PROJECT_CREATED)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].event_type, EventType.PROJECT_CREATED)
        self.assertEqual(events[0].data['title'], "Test Project")
    
    def test_event_listener(self):
        """Test event listener registration and callback."""
        received_events = []
        
        def callback(event):
            received_events.append(event)
        
        self.emitter.on(EventType.PROJECT_CREATED, callback)
        
        project = Project(
            title="Test Project",
            type=ProjectType.FEATURE,
            priority=Priority.P1,
            area=Area.REALTIME,
            sprint="Current",
            estimate=3
        )
        
        event = TelemetryEvent(
            event_type=EventType.PROJECT_CREATED,
            data=project.to_dict()
        )
        
        self.emitter.emit(event)
        
        self.assertEqual(len(received_events), 1)
        self.assertEqual(received_events[0].event_type, EventType.PROJECT_CREATED)
    
    def test_multiple_events(self):
        """Test emitting multiple events."""
        for i in range(3):
            project = Project(
                title=f"Project {i}",
                type=ProjectType.FEATURE,
                priority=Priority.P1,
                area=Area.REALTIME,
                sprint="Current",
                estimate=3
            )
            
            event = TelemetryEvent(
                event_type=EventType.PROJECT_CREATED,
                data=project.to_dict()
            )
            
            self.emitter.emit(event)
        
        all_events = self.emitter.get_events()
        self.assertEqual(len(all_events), 3)
        
        project_events = self.emitter.get_events(EventType.PROJECT_CREATED)
        self.assertEqual(len(project_events), 3)
    
    def test_event_to_dict(self):
        """Test converting event to dictionary."""
        project = Project(
            title="Test Project",
            type=ProjectType.FEATURE,
            priority=Priority.P1,
            area=Area.REALTIME,
            sprint="Current",
            estimate=3
        )
        
        event = TelemetryEvent(
            event_type=EventType.PROJECT_CREATED,
            data=project.to_dict()
        )
        
        event_dict = event.to_dict()
        
        self.assertEqual(event_dict['event_type'], "project.created")
        self.assertIn('data', event_dict)
        self.assertIn('timestamp', event_dict)
    
    def test_clear_events(self):
        """Test clearing events."""
        project = Project(
            title="Test Project",
            type=ProjectType.FEATURE,
            priority=Priority.P1,
            area=Area.REALTIME,
            sprint="Current",
            estimate=3
        )
        
        event = TelemetryEvent(
            event_type=EventType.PROJECT_CREATED,
            data=project.to_dict()
        )
        
        self.emitter.emit(event)
        self.assertEqual(len(self.emitter.get_events()), 1)
        
        self.emitter.clear()
        self.assertEqual(len(self.emitter.get_events()), 0)


if __name__ == '__main__':
    unittest.main()
