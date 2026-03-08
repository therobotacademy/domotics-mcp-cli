# PoC MCP Lighting Agent

Prueba de concepto de una capa C de domótica agentic para iluminación inteligente por habitaciones.

La PoC separa tres piezas:

1. **Servidor MCP-like** (`mcp_server/server.py`)
   - Expone tools genéricas para descubrir la casa, leer sensores y actuar sobre luces.
   - En esta versión el hogar está simulado en memoria.

2. **Agente** (`agent/agent.py`)
   - Descubre tools dinámicamente.
   - Construye un modelo de mundo por habitación.
   - Aplica guardarraíles.
   - Planifica acciones de iluminación.
   - Aprende preferencias simples a partir de overrides manuales.

3. **Demo runner** (`run_demo.py`)
   - Lanza varios escenarios guiados: presencia, noche, ausencia y corrección manual.

## Arquitectura lógica

```text
[Sensores/luces simulados]
          ↓
 [MCP-like tool server]
          ↓
   [Tool discovery]
          ↓
    [World model]
          ↓
    [Policy engine]
          ↓
        [Planner]
          ↓
       [Executor]
          ↓
    [Preference store]
```

## Tools expuestas por el servidor

- `list_tools`
- `describe_home`
- `get_room_state`
- `read_sensor`
- `get_device_state`
- `set_light`
- `set_room_lights`
- `report_manual_override`
- `set_sensor_value`
- `advance_time`

Las dos últimas son específicas de la simulación para poder demostrar casos en clase.

## Requisitos

```bash
pip install -r requirements.txt
```

## Ejecución

### Terminal 1: servidor

```bash
uvicorn mcp_server.server:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 2: demo completa

```bash
python run_demo.py
```

### Terminal 2 alternativa: agente continuo

```bash
python -m agent.agent
```

## Escenarios de la demo

1. Salón de noche con poca luz y presencia → encendido automático.
2. Dormitorio de noche → brillo limitado por política nocturna.
3. Ausencia sostenida → apagado automático.
4. Override manual → congelación temporal de automatización.
5. Aprendizaje de preferencia → el brillo preferido converge tras correcciones.

## Cómo sustituir la simulación por hardware real

Mantén intacto el contrato de tools y reemplaza las implementaciones internas del servidor:

- `read_sensor` → ESP32, Zigbee, Home Assistant, MQTT, etc.
- `set_light` / `set_room_lights` → bombillas reales, relés o actuadores.
- `report_manual_override` → eventos físicos de interruptor, app móvil, dashboard.

El agente no cambia mientras las tools MCP sigan siendo las mismas.

## Estructura

```text
poc_mcp_lighting/
├── agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── executor.py
│   ├── planner.py
│   ├── policy.py
│   ├── preferences.py
│   └── world_model.py
├── data/
│   └── preferences.db
├── mcp_server/
│   ├── __init__.py
│   └── server.py
├── shared/
│   ├── __init__.py
│   └── schemas.py
├── requirements.txt
├── run_demo.py
└── README.md
```
