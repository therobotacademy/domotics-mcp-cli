# =============================================================================
# Ejercicio C-3 — El executor y la lista blanca de tools  ★★☆
# Bloque C · Policy + Executor + Servidor
# =============================================================================
#
# CONTEXTO:
#   PlanExecutor en executor.py (líneas 6-17) tiene un conjunto SUPPORTED_TOOLS
#   que actúa como lista blanca: solo permite ejecutar las tools que están ahí.
#   Si el planner incluyera una tool no autorizada, el executor la rechaza.
#
#   SUPPORTED_TOOLS = {"set_room_lights", "set_light"}
#
#   Esto es un guardarraíl: aunque el planner (o en el futuro un LLM)
#   generara un plan con "reset" o "set_sensor_value", el executor lo bloquea.
#
# TAREA — PARTE 1: implementar PlanExecutor.execute()
#   Implementa el método execute() de PlanExecutor.
#   Si una action contiene una tool fuera de SUPPORTED_TOOLS,
#   lanza ValueError con el mensaje: "Unsupported tool in executor: <nombre>"
#
#   Usa el mock MCPClient que ya está definido (no necesitas el servidor real).
#
# TAREA — PARTE 2: razonamiento
#   Responde (en comentario) las preguntas al final del fichero.
#
# =============================================================================


class MockMCPClient:
    """Simula MCPClient sin hacer HTTP real."""
    def __init__(self):
        self.llamadas = []   # registro de cada call_tool recibido

    def call_tool(self, tool: str, args: dict) -> dict:
        self.llamadas.append({"tool": tool, "args": args})
        return {"ok": True, "tool": tool, "args": args}


class PlanExecutor:
    SUPPORTED_TOOLS = {"set_room_lights", "set_light"}

    def execute(self, mcp_client, plan: dict) -> list:
        """
        Ejecuta las acciones del plan llamando a mcp_client.call_tool().
        Lanza ValueError si una tool no está en SUPPORTED_TOOLS.
        Devuelve lista de respuestas.
        """
        # --- ESCRIBE TU CÓDIGO AQUÍ ---
        pass


# --- NO MODIFICAR DESDE AQUÍ ---
import traceback

def test(desc, plan, debe_fallar=False):
    client = MockMCPClient()
    executor = PlanExecutor()
    try:
        resultados = executor.execute(client, plan)
        if debe_fallar:
            print(f"  [FALLO] {desc}: debería haber lanzado ValueError pero no lo hizo")
            return
        ok = all(r.get("ok") for r in resultados)
        n_llamadas = len(client.llamadas)
        print(f"  [{'OK' if ok else 'FALLO'}] {desc}: {n_llamadas} tool(s) ejecutada(s)")
    except ValueError as e:
        if debe_fallar:
            print(f"  [OK] {desc}: ValueError lanzado correctamente → {e}")
        else:
            print(f"  [FALLO] {desc}: ValueError inesperado → {e}")

print("=== Tests de PlanExecutor ===\n")

test("Plan vacío (sin acciones)",
     {"room_id": "salon", "decision": "do_nothing", "actions": []})

test("set_room_lights (permitida)",
     {"room_id": "salon", "decision": "turn_on",
      "actions": [{"tool": "set_room_lights", "args": {"room_id": "salon", "on": True, "brightness": 25}}]})

test("set_light (permitida)",
     {"room_id": "salon", "decision": "turn_on",
      "actions": [{"tool": "set_light", "args": {"device_id": "light_salon_main", "on": True}}]})

test("set_sensor_value (NO permitida) → debe lanzar ValueError",
     {"room_id": "salon", "decision": "???",
      "actions": [{"tool": "set_sensor_value", "args": {"sensor_id": "pir_salon", "value": 1}}]},
     debe_fallar=True)

test("reset (NO permitida) → debe lanzar ValueError",
     {"room_id": "salon", "decision": "???",
      "actions": [{"tool": "reset", "args": {}}]},
     debe_fallar=True)


# ─────────────────────────────────────────────
# PARTE 2: preguntas (escribe tus respuestas aquí)
# ─────────────────────────────────────────────

# P1: ¿Por qué set_sensor_value NO está en SUPPORTED_TOOLS
#     aunque el servidor sí la expone?
# R:

# P2: ¿Por qué execute() recibe mcp_client como argumento
#     en lugar de crearlo internamente con MCPClient("http://...")?
# R:

# P3: Si en el futuro un LLM genera el plan en lugar del LightingPlanner,
#     ¿qué ventaja tiene que el executor tenga su propia lista blanca?
# R:
