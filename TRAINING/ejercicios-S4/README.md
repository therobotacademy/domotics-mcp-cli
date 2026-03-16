# Ejercicios — Sesión 4

## T05 Funciones · FastAPI cliente-servidor · Policy + Executor

Curso: Robótica Avanzada — EOI
Alumno: Manuel Ojeda
Fecha: 22 marzo 2026

---

## Estructura de carpetas

```
ejercicios/
│
├── README.md                  ← este fichero
│
├── A1_clamp_brightness.py     ┐
├── A2_should_turn_off.py      │  Bloque A — T05 Funciones
├── A3_args_defecto.py         │  (completar y ejecutar, sin servidor)
├── A4_scope_mutables.py       ┘
│
├── B1_get_describe_home.py    ┐  Bloque B — FastAPI cliente-servidor
├── B2_call_tool_post.py       ┘  (requieren servidor en localhost:8000)
│
├── C1_apply_policy.py         ┐
├── C2_trazar_dispatcher.py    │  Bloque C — Policy + Executor + Servidor
├── C3_executor_lista_blanca.py│  (A/C: sin servidor · B: con servidor)
├── C4_nuevo_endpoint.py       ┘
│
└── soluciones/                ← no abrir hasta intentarlo
    ├── A1_clamp_brightness_sol.py
    ├── A2_should_turn_off_sol.py
    ├── A3_args_defecto_sol.py
    ├── A4_scope_mutables_sol.py
    ├── B1_get_describe_home_sol.py
    ├── B2_call_tool_post_sol.py
    ├── C1_apply_policy_sol.py
    ├── C2_trazar_dispatcher_sol.py
    ├── C3_executor_lista_blanca_sol.py
    └── C4_nuevo_endpoint_sol.py
```

---

## Cómo usar estos ejercicios

1. **Abre el fichero** en orden (A1 → C4).
2. **Lee CONTEXTO y TAREA** — siempre explican de dónde viene el código real.
3. **Escribe tu código** donde está `# --- ESCRIBE TU CÓDIGO AQUÍ ---`.
4. **Ejecuta** con `python NombreEjercicio.py`.
5. Los ejercicios con comprobación automática imprimen `[OK]` o `[FALLO]`.
6. Consulta `soluciones/` solo si te bloqueas más de 10 minutos.

---

## Dificultad

| Símbolo | Nivel                                                              |
| -------- | ------------------------------------------------------------------ |
| ★☆☆   | Básico — traslación directa del material teórico               |
| ★★☆   | Intermedio — combina conceptos o requiere leer código del agente |
| ★★★   | Avanzado — varios pasos o razonamiento arquitectónico            |

---

## Ejercicios que necesitan el servidor

Los siguientes requieren que el servidor MCP esté corriendo:

```bash
# Abre una terminal, ve a Domotics-MCP-cli y ejecuta:
uvicorn mcp_server.server:app --reload --port 8000
```

| Ejercicio | Necesita servidor |
| --------- | :---------------: |
| A1 – A4  |        No        |
| B1        |        Sí        |
| B2        |        Sí        |
| C1 – C4  |        No        |

---

## Relación con el código del agente

| Ejercicio | Archivo del agente           | Líneas            |
| --------- | ---------------------------- | ------------------ |
| A-1       | `agent/policy.py`          | 40–43             |
| A-2       | `agent/policy.py`          | 30–37             |
| A-3       | `agent/preferences.py`     | 46 (firma)         |
| A-4       | `agent/agent.py`           | 108 (`.copy()`)  |
| B-1       | `agent/agent.py` MCPClient | 29–30             |
| B-2       | `agent/agent.py` MCPClient | 35–38             |
| C-1       | `agent/policy.py`          | 16–27             |
| C-2       | `mcp_server/server.py`     | 141–170           |
| C-3       | `agent/executor.py`        | 6–17              |
| C-4       | `mcp_server/server.py`     | estructura general |

---

## Conceptos de T05 en el código

| Concepto                          | Ejemplo en el agente                             |
| --------------------------------- | ------------------------------------------------ |
| Función sin retorno              | `_log()` — escribe, no devuelve nada útil    |
| Args posicionales + return        | `clamp_brightness(time_bucket, brightness)`    |
| Return condicional (early return) | `_parse_ts(ts)` — si ts es None devuelve None |
| Return múltiple paths            | `apply_policy()` — tres return posibles       |
| Arg con valor por defecto         | `update_preference(..., alpha=0.3)`            |
| Keyword args en llamada           | `json.dumps(p, ensure_ascii=False, indent=2)`  |
| Variable de módulo (scope)       | `NIGHT_MAX_BRIGHTNESS = 30` en policy.py       |
| Mutable por referencia            | por eso `_log()` usa `payload.copy()`        |

---

## Tarea adicional

- Completa C-4 añadiendo el endpoint `/status` a `mcp_server/server.py` de verdad.
  Verifica que aparece en `http://127.0.0.1:8000/docs` (Swagger UI).
- Cambia `ABSENCE_OFF_DELAY_MIN = 3` a `1` en `policy.py` y vuelve a ejecutar
  `run_demo.py`. ¿Qué cambia en el Escenario 3?
- Adelanto sesión 5: lee `agent/agent.py` completo y fíjate en `LightingAgent`,
  `PreferenceStore`, `PlanExecutor`, `LightingPlanner`.
  Son **clases**. ¿Qué tienen en común? ¿Para qué sirve `__init__`?
