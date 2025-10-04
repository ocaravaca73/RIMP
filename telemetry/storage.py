"""
Storage backends for telemetry data
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
import json

from .models import TelemetryData, TelemetryEvent, TelemetryMetric


class TelemetryStorage(ABC):
    """Abstract base class for telemetry storage backends"""
    
    @abstractmethod
    def store(self, data: TelemetryData) -> None:
        """Store telemetry data"""
        pass
    
    @abstractmethod
    def retrieve(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> TelemetryData:
        """Retrieve telemetry data within a time range"""
        pass


class MemoryStorage(TelemetryStorage):
    """In-memory storage backend"""
    
    def __init__(self):
        self._events: List[TelemetryEvent] = []
        self._metrics: List[TelemetryMetric] = []
    
    def store(self, data: TelemetryData) -> None:
        """Store telemetry data in memory"""
        self._events.extend(data.events)
        self._metrics.extend(data.metrics)
    
    def retrieve(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> TelemetryData:
        """Retrieve telemetry data from memory"""
        events = self._events
        metrics = self._metrics
        
        # Filter by time range
        if start_time:
            events = [e for e in events if e.timestamp >= start_time]
            metrics = [m for m in metrics if m.timestamp >= start_time]
        
        if end_time:
            events = [e for e in events if e.timestamp <= end_time]
            metrics = [m for m in metrics if m.timestamp <= end_time]
        
        # Apply limit
        if limit:
            events = events[:limit]
            metrics = metrics[:limit]
        
        return TelemetryData(events=events, metrics=metrics)
    
    def clear(self) -> None:
        """Clear all stored data"""
        self._events.clear()
        self._metrics.clear()


class FileStorage(TelemetryStorage):
    """File-based storage backend"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def _serialize_event(self, event: TelemetryEvent) -> dict:
        """Serialize event to JSON-compatible dict"""
        return {
            'event_id': event.event_id,
            'timestamp': event.timestamp.isoformat(),
            'event_type': event.event_type.value if hasattr(event.event_type, 'value') else str(event.event_type),
            'source': event.source,
            'message': event.message,
            'metadata': event.metadata
        }
    
    def _serialize_metric(self, metric: TelemetryMetric) -> dict:
        """Serialize metric to JSON-compatible dict"""
        return {
            'metric_id': metric.metric_id,
            'timestamp': metric.timestamp.isoformat(),
            'name': metric.name,
            'value': metric.value,
            'unit': metric.unit,
            'tags': metric.tags
        }
    
    def store(self, data: TelemetryData) -> None:
        """Append telemetry data to file"""
        with open(self.file_path, 'a') as f:
            for event in data.events:
                f.write(json.dumps({
                    'type': 'event',
                    'data': self._serialize_event(event)
                }) + '\n')
            
            for metric in data.metrics:
                f.write(json.dumps({
                    'type': 'metric',
                    'data': self._serialize_metric(metric)
                }) + '\n')
    
    def retrieve(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> TelemetryData:
        """Retrieve telemetry data from file"""
        events = []
        metrics = []
        count = 0
        
        try:
            with open(self.file_path, 'r') as f:
                for line in f:
                    if limit and count >= limit:
                        break
                    
                    try:
                        item = json.loads(line.strip())
                        if item['type'] == 'event':
                            data = item['data']
                            # Convert timestamp string back to datetime
                            if isinstance(data.get('timestamp'), str):
                                from dateutil import parser
                                data['timestamp'] = parser.parse(data['timestamp'])
                            events.append(TelemetryEvent(**data))
                            count += 1
                        elif item['type'] == 'metric':
                            data = item['data']
                            # Convert timestamp string back to datetime
                            if isinstance(data.get('timestamp'), str):
                                from dateutil import parser
                                data['timestamp'] = parser.parse(data['timestamp'])
                            metrics.append(TelemetryMetric(**data))
                            count += 1
                    except (json.JSONDecodeError, KeyError, Exception):
                        continue
        except FileNotFoundError:
            pass
        
        return TelemetryData(events=events, metrics=metrics)
