# Solución — Ejercicio C-2

# ─────────────────────────────────────────────
# PARTE 1: Respuestas correctas
# ─────────────────────────────────────────────

respuesta_clase_pydantic   = "ToolCallRequest"
respuesta_linea_branch     = 168         # línea: if tool == "advance_time":
respuesta_funcion_llamada  = "_advance_time(args['minutes'])"
respuesta_retorno          = {"ok": True, "now": "2026-03-08T21:05:00"}


# ─────────────────────────────────────────────
# PARTE 2: Mini-dispatcher
# ─────────────────────────────────────────────

from datetime import datetime, timedelta

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
    if tool == "advance_time":
        return _advance_time(args["minutes"])
    if tool == "reset":
        return _reset()
    if tool == "get_now":
        return {"ok": True, "now": _estado["now"].isoformat()}
    return {"ok": False, "error": f"Unknown tool: {tool}"}


# Verificación
print("=== PARTE 1 ===")
respuestas_p1 = [
    ("Clase Pydantic",     respuesta_clase_pydantic,   "ToolCallRequest"),
    ("Línea del branch",   str(respuesta_linea_branch),"168"),
    ("Función privada",    respuesta_funcion_llamada,  "_advance_time(args['minutes'])"),
    ("Retorno tiene 'ok'", "ok" in respuesta_retorno,  True),
]
for desc, obtenido, esperado in respuestas_p1:
    ok = obtenido == esperado
    print(f"  [{'OK' if ok else '???'}] {desc}")

print("\n=== PARTE 2 ===")
errores = 0
pruebas = [
    ("advance_time 10 min", "advance_time", {"minutes": 10},
     lambda r: r.get("ok") and "21:10" in r.get("now", "")),
    ("reset",               "reset",        {},
     lambda r: r.get("ok") is True),
    ("tool desconocida",    "borrar_todo",  {},
     lambda r: r.get("ok") is False),
]
for desc, tool, args, check in pruebas:
    resultado = dispatch(tool, args)
    ok = check(resultado)
    if not ok: errores += 1
    print(f"  [{'OK' if ok else 'FALLO'}] {desc}: {resultado}")

print("\nParte 2 correcta." if errores == 0 else f"{errores} error(es).")
