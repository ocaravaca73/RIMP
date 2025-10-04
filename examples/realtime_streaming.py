"""
Real-time streaming example
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from telemetry import TelemetryCollector, TelemetryConfig, EventType
from telemetry.streaming import TelemetryStream
from telemetry.storage import MemoryStorage
import time
import random


def print_consumer(data):
    """Consumer that prints telemetry data"""
    if data.events:
        print(f"\n[STREAM] Received {len(data.events)} events:")
        for event in data.events[:3]:  # Show first 3
            print(f"  {event.timestamp.isoformat()} - {event.message}")
    
    if data.metrics:
        print(f"[STREAM] Received {len(data.metrics)} metrics:")
        for metric in data.metrics[:3]:  # Show first 3
            print(f"  {metric.name}: {metric.value} {metric.unit or ''}")


def main():
    """Demonstrate real-time telemetry streaming"""
    
    print("Starting real-time telemetry streaming example...")
    
    # Create configuration for real-time mode
    config = TelemetryConfig(
        enabled=True,
        buffer_size=50,
        flush_interval=2.0,
        realtime_mode=True
    )
    
    # Create collector and storage
    collector = TelemetryCollector(config)
    storage = MemoryStorage()
    
    # Create and start stream
    stream = TelemetryStream(collector, storage, interval=1.0)
    stream.add_consumer(print_consumer)
    stream.start()
    
    print("Stream started. Generating telemetry data...\n")
    
    # Simulate application generating telemetry data
    try:
        for i in range(20):
            # Generate random metrics
            cpu = random.uniform(20, 90)
            memory = random.uniform(1000, 8000)
            requests = random.randint(10, 200)
            
            collector.collect_metric("cpu_usage", cpu, "percent", {"host": "server-01"})
            collector.collect_metric("memory_usage", memory, "MB", {"host": "server-01"})
            collector.collect_metric("request_count", requests, "requests")
            
            # Occasionally generate events
            if i % 5 == 0:
                collector.collect_event(
                    source="monitor",
                    message=f"Checkpoint {i}: System healthy",
                    event_type=EventType.INFO
                )
            
            if cpu > 80:
                collector.collect_event(
                    source="monitor",
                    message=f"High CPU usage: {cpu:.1f}%",
                    event_type=EventType.WARNING,
                    metadata={"cpu": cpu}
                )
            
            time.sleep(0.5)
        
        # Give time for final flush
        time.sleep(2)
        
    finally:
        # Stop stream
        print("\nStopping stream...")
        stream.stop()
        print("Stream stopped.")
        
        # Show storage statistics
        stored_data = storage.retrieve()
        print(f"\nTotal stored: {len(stored_data.events)} events, {len(stored_data.metrics)} metrics")


if __name__ == "__main__":
    main()
