# Ejercicios — Sesión 3

## T03 Cadenas · T04 Ficheros · Introducción a Domotics-MCP-cli


```
ejercicios/
│
├── README.md                  ← este fichero
│
├── datos_demo/
│   └── agent_log_ejemplo.jsonl   ← log de ejemplo para C-3 si no tienes el real
│
├── A1_sensores.py             ┐
├── A2_time_bucket.py          │  Bloque A — T03 Cadenas
├── A3_sensor_ids.py           │  (completar y ejecutar)
├── A4_parsear_log.py          ┘
│
├── B1_log_jsonl.py            ┐
├── B2_preferencias_sqlite.py  │  Bloque B — T04 Ficheros
├── B3_suavizado.py            ┘
│
├── C1_trazar_ciclo.py         ┐
├── C2_log_con_timestamp.py    │  Bloque C — Domotics-MCP-cli
├── C3_resumen_log.py          │  (leer código + completar)
├── C4_nueva_habitacion.py     ┘
│
└── soluciones/                ← no abrir hasta intentarlo
    ├── A1_sensores_sol.py
    ├── A2_time_bucket_sol.py
    ├── A3_sensor_ids_sol.py
    ├── A4_parsear_log_sol.py
    ├── B1_log_jsonl_sol.py
    ├── B2_preferencias_sqlite_sol.py
    ├── B3_suavizado_sol.py
    ├── C1_trazar_ciclo_sol.py
    ├── C2_log_con_timestamp_sol.py
    ├── C3_resumen_log_sol.py
    └── C4_nueva_habitacion_sol.py
```

---

## Cómo usar estos ejercicios

1. **Abre el fichero** del ejercicio que te toque (por orden, de A1 a C4).
2. **Lee el bloque CONTEXTO** al principio — explica de dónde viene el código.
3. **Lee el bloque TAREA** — te dice exactamente qué tienes que escribir.
4. **Escribe tu código** en la zona marcada `# --- ESCRIBE TU CÓDIGO AQUÍ ---`.
5. **Ejecuta el script** desde la terminal:
   ```
   python A1_sensores.py
   ```
6. Los ejercicios con comprobación automática imprimirán `[OK]` o `[FALLO]`.
7. **Solo si te bloqueas**, consulta la solución en `soluciones/`.

---

## Dificultad

| Símbolo | Nivel                                                      |
| -------- | ---------------------------------------------------------- |
| ★☆☆   | Básico — directamente del material teórico              |
| ★★☆   | Intermedio — combina conceptos o requiere navegar un dict |
| ★★★   | Avanzado — lógica más elaborada o varios pasos          |

---

## Relación con el código del agente

Cada ejercicio replica o extiende un fragmento real de `Domotics-MCP-cli/`.
Si resuelves todos, comprenderás exactamente cómo funciona el agente.

| Ejercicio | Archivo del agente                        | Líneas  |
| --------- | ----------------------------------------- | -------- |
| A-1       | `agent/world_model.py`                  | 19–20   |
| A-2       | `agent/world_model.py`                  | 7–14    |
| A-3       | `mcp_server/server.py`                  | 15–62   |
| A-4       | `agent/agent.py`                        | 106–109 |
| B-1       | `agent/agent.py`                        | 106–109 |
| B-2       | `agent/preferences.py`                  | 36–44   |
| B-3       | `agent/preferences.py`                  | 46–60   |
| C-1       | `agent/planner.py` + `world_model.py` | —       |
| C-2       | `agent/agent.py`                        | 106–109 |
| C-3       | `agent/agent.py` + log real             | —       |
| C-4       | `mcp_server/server.py`                  | 15–62   |

---

## Prerrequisitos para ejecutar C-3 con el log real

Antes de C-3, ejecuta el servidor y el demo desde la carpeta `Domotics-MCP-cli/`:

```bash
# Terminal 1
cd Domotics-MCP-cli
uvicorn mcp_server.server:app --reload --port 8000

# Terminal 2
cd Domotics-MCP-cli
python run_demo.py
```

Si no puedes ejecutarlo ahora, C-3 usa automáticamente el fichero de ejemplo
`datos_demo/agent_log_ejemplo.jsonl`.

---

## Tarea opcional

- Ejecuta `run_demo.py` en tu máquina y repite C-3 con el log real.
- En C-4 ya definiste la cocina en Python. Ahora añádela de verdad en
  `mcp_server/server.py` (sección `STATE`) y comprueba que el demo sigue
  funcionando con cuatro habitaciones.
- Adelanto sesión 4: lee `agent/policy.py` completo. ¿Qué hace `apply_policy`?
  ¿Cuándo bloquea al agente?
