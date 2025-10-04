"""
Custom storage backend example
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from telemetry import TelemetryCollector, TelemetryConfig, EventType
from telemetry.storage import FileStorage
from telemetry.streaming import TelemetryStream
import tempfile
import time


def main():
    """Demonstrate custom file storage backend"""
    
    # Create temporary file for storage
    temp_file = os.path.join(tempfile.gettempdir(), "telemetry_data.jsonl")
    print(f"Using storage file: {temp_file}")
    
    # Create configuration
    config = TelemetryConfig(
        enabled=True,
        buffer_size=5,
        realtime_mode=True
    )
    
    # Create collector and file storage
    collector = TelemetryCollector(config)
    storage = FileStorage(temp_file)
    
    # Create stream with file storage
    stream = TelemetryStream(collector, storage, interval=1.0)
    
    # Add consumer to track what's being stored
    def storage_consumer(data):
        if data.events or data.metrics:
            print(f"Storing: {len(data.events)} events, {len(data.metrics)} metrics")
    
    stream.add_consumer(storage_consumer)
    stream.start()
    
    print("\nGenerating telemetry data...")
    
    # Generate some telemetry data
    for i in range(10):
        collector.collect_event(
            source="app",
            message=f"Event {i+1}",
            event_type=EventType.INFO
        )
        
        collector.collect_metric(
            name="counter",
            value=float(i+1),
            tags={"iteration": str(i+1)}
        )
        
        time.sleep(0.3)
    
    # Wait for final flush
    time.sleep(2)
    stream.stop()
    
    # Read back from storage
    print("\nReading back from storage...")
    read_storage = FileStorage(temp_file)
    data = read_storage.retrieve()
    
    print(f"\nRead {len(data.events)} events:")
    for event in data.events[:5]:
        print(f"  - {event.message}")
    
    print(f"\nRead {len(data.metrics)} metrics:")
    for metric in data.metrics[:5]:
        print(f"  - {metric.name}: {metric.value}")
    
    print(f"\nData persisted to: {temp_file}")
    print("Example completed!")


if __name__ == "__main__":
    main()
