"""
Example: Basic Telemetry Usage
Demonstrates how to use the telemetry system
"""

from telemetry.core import TelemetryService
from telemetry.config import load_config


def main():
    # Initialize telemetry service with default config
    config = load_config()
    telemetry = TelemetryService(config)
    
    # Start the service
    telemetry.start()
    print("Telemetry service started")
    
    # Emit some sample events
    telemetry.emit(
        event_type='system.startup',
        source='example-app',
        data={'version': '1.0.0', 'environment': 'development'}
    )
    
    telemetry.emit(
        event_type='user.action',
        source='example-app',
        data={'action': 'login', 'user_id': 'user123'},
        metadata={'ip': '192.168.1.1'}
    )
    
    telemetry.emit(
        event_type='system.metric',
        source='example-app',
        data={'cpu_usage': 45.2, 'memory_usage': 1024}
    )
    
    # Retrieve and display events
    events = telemetry.get_events(batch_size=10)
    print(f"\nCollected {len(events)} events:")
    for event in events:
        print(f"  - [{event['event_type']}] from {event['source']}")
        print(f"    Data: {event['data']}")
    
    # Display statistics
    stats = telemetry.get_stats()
    print(f"\nTelemetry Statistics:")
    print(f"  Total events: {stats['total_events_collected']}")
    print(f"  Buffer size: {stats['current_buffer_size']}/{stats['max_buffer_size']}")
    print(f"  Status: {'Running' if stats['running'] else 'Stopped'}")
    
    # Stop the service
    telemetry.stop()
    print("\nTelemetry service stopped")


if __name__ == '__main__':
    main()
