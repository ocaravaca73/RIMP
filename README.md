# RIMP - Real-time Telemetry System

Sistema de telemetría en tiempo real para recopilación, procesamiento y almacenamiento de métricas y eventos.

## Características

- **Recopilación de Eventos**: Captura eventos con tipos (info, warning, error, debug) y metadatos
- **Métricas en Tiempo Real**: Recolección de métricas con valores numéricos, unidades y etiquetas
- **Streaming en Tiempo Real**: Transmisión continua de datos de telemetría a consumidores
- **Almacenamiento Flexible**: Backends de almacenamiento en memoria o archivo
- **Thread-Safe**: Operaciones seguras para entornos multi-hilo
- **Configurable**: Sistema de configuración flexible para diferentes casos de uso

## Instalación

```bash
pip install -r requirements.txt
```

## Uso Básico

### Recopilación de Eventos

```python
from telemetry import TelemetryCollector, TelemetryConfig, EventType

# Crear colector
config = TelemetryConfig(enabled=True, realtime_mode=True)
collector = TelemetryCollector(config)

# Recopilar evento
collector.collect_event(
    source="api_server",
    message="Request received",
    event_type=EventType.INFO,
    metadata={"endpoint": "/api/users", "method": "GET"}
)
```

### Recopilación de Métricas

```python
# Recopilar métrica
collector.collect_metric(
    name="response_time",
    value=125.5,
    unit="ms",
    tags={"endpoint": "/api/users", "status": "200"}
)
```

### Streaming en Tiempo Real

```python
from telemetry.streaming import TelemetryStream
from telemetry.storage import MemoryStorage

# Crear stream con almacenamiento
storage = MemoryStorage()
stream = TelemetryStream(collector, storage, interval=1.0)

# Agregar consumidor
def print_telemetry(data):
    print(f"Events: {len(data.events)}, Metrics: {len(data.metrics)}")

stream.add_consumer(print_telemetry)

# Iniciar stream
stream.start()

# ... tu aplicación ...

# Detener stream
stream.stop()
```

## Configuración

```python
from telemetry import TelemetryConfig

config = TelemetryConfig(
    enabled=True,              # Habilitar telemetría
    buffer_size=100,           # Tamaño del buffer
    flush_interval=5.0,        # Intervalo de flush en segundos
    realtime_mode=True,        # Modo tiempo real
    storage_backend="memory",  # Backend: memory, file, database
    storage_path=None          # Ruta para almacenamiento en archivo
)
```

## Arquitectura

```
┌─────────────────┐
│   Application   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Collector    │◄─── Config
└────────┬────────┘
         │
         ├─────► Buffer
         │
         ▼
┌─────────────────┐
│     Stream      │
└────────┬────────┘
         │
         ├─────► Storage
         │
         └─────► Consumers
```

## Ejemplos

Ver el directorio `examples/` para casos de uso completos:
- `basic_usage.py`: Uso básico de telemetría
- `realtime_streaming.py`: Streaming en tiempo real
- `custom_storage.py`: Implementación de storage personalizado

## Desarrollo

### Tests

```bash
pytest tests/
```

### Estructura del Proyecto

```
telemetry/
├── __init__.py          # API pública
├── models.py            # Modelos de datos
├── config.py            # Configuración
├── collector.py         # Colector de telemetría
├── storage.py           # Backends de almacenamiento
└── streaming.py         # Streaming en tiempo real
```

## Licencia

MIT
