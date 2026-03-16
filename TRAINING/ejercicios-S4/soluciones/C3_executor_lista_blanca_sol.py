# Solución — Ejercicio C-3

class MockMCPClient:
    def __init__(self):
        self.llamadas = []

    def call_tool(self, tool: str, args: dict) -> dict:
        self.llamadas.append({"tool": tool, "args": args})
        return {"ok": True, "tool": tool, "args": args}


class PlanExecutor:
    SUPPORTED_TOOLS = {"set_room_lights", "set_light"}

    def execute(self, mcp_client, plan: dict) -> list:
        results = []
        for action in plan["actions"]:
            tool = action["tool"]
            if tool not in self.SUPPORTED_TOOLS:
                raise ValueError(f"Unsupported tool in executor: {tool}")
            res = mcp_client.call_tool(tool, action["args"])
            results.append(res)
        return results


# Verificación
def test(desc, plan, debe_fallar=False):
    client   = MockMCPClient()
    executor = PlanExecutor()
    try:
        resultados = executor.execute(client, plan)
        if debe_fallar:
            print(f"  [FALLO] {desc}: debería haber lanzado ValueError")
            return
        print(f"  [OK] {desc}: {len(client.llamadas)} tool(s) ejecutada(s)")
    except ValueError as e:
        if debe_fallar:
            print(f"  [OK] {desc}: ValueError → {e}")
        else:
            print(f"  [FALLO] {desc}: ValueError inesperado → {e}")

test("Plan vacío",          {"room_id": "salon", "decision": "do_nothing", "actions": []})
test("set_room_lights",     {"room_id": "salon", "decision": "turn_on",
                              "actions": [{"tool": "set_room_lights", "args": {"room_id": "salon", "on": True}}]})
test("set_light",           {"room_id": "salon", "decision": "turn_on",
                              "actions": [{"tool": "set_light", "args": {"device_id": "light_salon_main", "on": True}}]})
test("set_sensor_value → ValueError",
                            {"room_id": "salon", "decision": "???",
                              "actions": [{"tool": "set_sensor_value", "args": {}}]},
     debe_fallar=True)
test("reset → ValueError",  {"room_id": "salon", "decision": "???",
                              "actions": [{"tool": "reset", "args": {}}]},
     debe_fallar=True)


# ─────────────────────────────────────────────
# PARTE 2: Respuestas correctas
# ─────────────────────────────────────────────

# P1: set_sensor_value es una tool de SIMULACIÓN, no de control.
#     El agente no debe poder modificar sensores: eso solo lo hace el entorno real
#     o el script de demo. Si el agente pudiera hacerlo, podría "engañar" a su
#     propio world model fabricando lecturas falsas.

# P2: Porque así el executor es reutilizable en tests con un MockMCPClient
#     (como hacemos aquí) sin necesitar un servidor real. Es el patrón
#     "inyección de dependencias": el colaborador se pasa desde fuera.

# P3: Un LLM puede generar texto arbitrario como nombre de tool.
#     La lista blanca garantiza que aunque el LLM alucinara y generara
#     "apagar_alarma" o "reset", el executor lo rechazaría.
#     Separar planner y executor significa que el LLM nunca tiene acceso
#     directo al servidor: siempre pasa por el guardarraíl.
