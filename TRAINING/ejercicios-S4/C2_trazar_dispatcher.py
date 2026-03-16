# =============================================================================
# Ejercicio C-2 — Trazar el dispatcher POST /call_tool  ★★☆
# Bloque C · Policy + Executor + Servidor
# =============================================================================
#
# CONTEXTO:
#   El endpoint POST /call_tool de server.py (líneas 141-170) es un dispatcher:
#   recibe el nombre de una tool y delega en la función privada correspondiente.
#
#   Este patrón es fundamental en el diseño MCP: el agente no llama a 10 URLs
#   distintas, sino que siempre usa la misma URL con el nombre de la tool.
#
# TAREA — PARTE 1: trazar a mano
#   Para la petición:
#       POST /call_tool
#       {"tool": "advance_time", "args": {"minutes": 5}}
#
#   Responde las preguntas completando las variables de abajo.
#   Consulta server.py para encontrar las respuestas.
#
# TAREA — PARTE 2: mini-dispatcher
#   Implementa un dispatcher simplificado que sea funcionalmente equivalente
#   al de server.py, pero sin FastAPI (sólo Python puro).
#
# =============================================================================

# ─────────────────────────────────────────────
# PARTE 1: preguntas (completa las variables)
# ─────────────────────────────────────────────

# P1: ¿Qué clase Pydantic valida el cuerpo de la petición? (ver server.py línea 141)
respuesta_clase_pydantic = "???"

# P2: Dentro de call_tool(), ¿en qué rama del if/elif entra
#     cuando tool == "advance_time"? (escribe el número de línea de server.py)
respuesta_linea_branch = 0

# P3: ¿Qué función privada se llama y con qué argumento?
#     Formato: "_nombre_funcion(argumento)"
respuesta_funcion_llamada = "???"

# P4: ¿Qué devuelve _advance_time() cuando todo va bien?
#     (mira server.py líneas 219-224 y escribe un ejemplo del dict devuelto)
respuesta_retorno = {}


# ─────────────────────────────────────────────
# PARTE 2: mini-dispatcher (implementa)
# ─────────────────────────────────────────────

from datetime import datetime, timedelta

# Estado mínimo del servidor (versión simplificada)
_estado = {
    "now": datetime(2026, 3, 8, 21, 0, 0),
    "contador_resets": 0,
}


def _advance_time(minutes: int) -> dict:
    if minutes < 0:
        return {"ok": False, "error": "minutes must be >= 0"}
    _estado["now"] = _estado["now"] + timedelta(minutes=minutes)
    return {"ok": True, "now": _estado["now"].isoformat()}


def _reset() -> dict:
    _estado["now"] = datetime(2026, 3, 8, 21, 0, 0)
    _estado["contador_resets"] += 1
    return {"ok": True, "resets": _estado["contador_resets"]}


def dispatch(tool: str, args: dict) -> dict:
    """
    Dispatcher que enruta 'tool' a la función correcta.
    Tools soportadas: "advance_time", "reset", "get_now".

    Si la tool no existe, devuelve {"ok": False, "error": "Unknown tool: <nombre>"}.

    TAREA: implementa el dispatcher usando if/elif.
    """
    # --- ESCRIBE TU CÓDIGO AQUÍ ---
    pass


# --- NO MODIFICAR DESDE AQUÍ ---
print("=== PARTE 1: Respuestas de comprensión ===")
respuestas_p1 = [
    ("Clase Pydantic",         respuesta_clase_pydantic,    "ToolCallRequest"),
    ("Línea del branch",       str(respuesta_linea_branch), "168"),
    ("Función privada",        respuesta_funcion_llamada,   "_advance_time(args['minutes'])"),
    ("Retorno advance_time",   "ok" in respuesta_retorno,   True),
]
for desc, obtenido, esperado in respuestas_p1:
    ok = obtenido == esperado
    print(f"  [{'OK' if ok else '???'}] {desc}: {obtenido!r}  (esperado: {esperado!r})")

print("\n=== PARTE 2: Mini-dispatcher ===")
errores = 0
pruebas = [
    ("advance_time 10 min",  "advance_time", {"minutes": 10},  lambda r: r.get("ok") and "21:10" in r.get("now", "")),
    ("reset",                "reset",        {},                lambda r: r.get("ok") is True),
    ("tool desconocida",     "borrar_todo",  {},                lambda r: r.get("ok") is False),
]
for desc, tool, args, check in pruebas:
    resultado = dispatch(tool, args)
    ok = check(resultado) if resultado is not None else False
    if not ok:
        errores += 1
    print(f"  [{'OK' if ok else 'FALLO'}] {desc}: {resultado}")

print()
print("Parte 2 correcta." if errores == 0 else f"{errores} caso(s) incorrecto(s) en Parte 2.")
