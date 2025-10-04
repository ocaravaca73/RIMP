"""
Telemetry Configuration
Default configuration for the telemetry system
"""

DEFAULT_CONFIG = {
    # Enable/disable telemetry collection
    'enabled': True,
    
    # Buffer size for event collection
    'buffer_size': 1000,
    
    # Batch size for event processing
    'batch_size': 10,
    
    # Source identifier for this instance
    'source_id': 'isbl-telemetry',
    
    # Event types to collect (empty list = all types)
    'event_types': [],
    
    # Sampling rate (1.0 = all events, 0.5 = 50% of events)
    'sampling_rate': 1.0,
}


def load_config(custom_config: dict = None) -> dict:
    """
    Load telemetry configuration.
    
    Args:
        custom_config: Custom configuration to override defaults
        
    Returns:
        Merged configuration dictionary
    """
    config = DEFAULT_CONFIG.copy()
    if custom_config:
        config.update(custom_config)
    return config
