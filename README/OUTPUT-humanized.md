El output consiste enun  **ciclo de percepción → decisión → acción → aprendizaje → bloqueo temporal**

## 1) Diagrama global de la demo

```text
                    ┌──────────────────────────────────────┐
                    │         MCP SERVER / CASA            │
                    │──────────────────────────────────────│
                    │ Tools descubiertas:                  │
                    │ - list_tools                         │
                    │ - describe_home                      │
                    │ - get_room_state                     │
                    │ - read_sensor                        │
                    │ - get_device_state                   │
                    │ - set_light / set_room_lights        │
                    │ - report_manual_override             │
                    │ - set_sensor_value                   │
                    │ - advance_time                       │
                    └──────────────────────────────────────┘
                                      │
                                      │ 1) discovery + lectura de estado
                                      ▼
                    ┌──────────────────────────────────────┐
                    │         AGENTE - WORLD MODEL         │
                    │──────────────────────────────────────│
                    │ Construye por habitación:            │
                    │ - occupied / occupied_confidence     │
                    │ - lux                                │
                    │ - time_bucket = night                │
                    │ - estado actual de la luz            │
                    │ - preferencias aprendidas            │
                    │ - meta: override / cooldown /        │
                    │   absence_since                      │
                    └──────────────────────────────────────┘
                                      │
                                      │ 2) política
                                      ▼
                    ┌──────────────────────────────────────┐
                    │          POLICY ENGINE               │
                    │──────────────────────────────────────│
                    │ Reglas de bloqueo:                   │
                    │ - cooldown                           │
                    │ - ventana de override manual         │
                    │ - histéresis de ausencia             │
                    └──────────────────────────────────────┘
                         │                  │                    │
                         │ allowed          │ blocked            │ noop
                         ▼                  ▼                    ▼
          ┌────────────────────────┐  ┌───────────────┐  ┌──────────────────┐
          │        PLANNER         │  │   BLOQUEADO   │  │   NO HACER NADA  │
          │────────────────────────│  │               │  │                  │
          │ Decide plan:           │  │ policy_reason │  │ contexto ya       │
          │ - turn_on              │  │               │  │ satisfecho o      │
          │ - turn_off             │  │               │  │ ausencia aún corta│
          │ - do_nothing           │  └───────────────┘  └──────────────────┘
          └────────────────────────┘
                         │
                         │ 3) acciones MCP
                         ▼
          ┌───────────────────────────────────────────────┐
          │                 EXECUTOR                      │
          │───────────────────────────────────────────────│
          │ Llama a tools como:                           │
          │ - set_room_lights(room_id, on, brightness)    │
          │ - verifica resultado                          │
          └───────────────────────────────────────────────┘
                         │
                         │ 4) cambio real del estado
                         ▼
          ┌───────────────────────────────────────────────┐
          │              EVENTOS / LOGS                   │
          │───────────────────────────────────────────────│
          │ sensor_update                                 │
          │ set_light                                     │
          │ time_advanced                                 │
          │ manual_override                               │
          └───────────────────────────────────────────────┘
                         │
                         │ 5) feedback humano
                         ▼
          ┌───────────────────────────────────────────────┐
          │         PREFERENCE LEARNER                    │
          │───────────────────────────────────────────────│
          │ Ejemplo: dormitorio night                     │
          │ preferencia 21  ──ajuste humano──> 18         │
          └───────────────────────────────────────────────┘
```

## 2) Diagrama temporal de los escenarios

```text
TIEMPO ─────────────────────────────────────────────────────────────────────────────>

21:00
│
├─ Descubrimiento de tools
│   El agente ve qué puede hacer y cómo leer la casa.
│
├─ Estado inicial casa
│   - salón: PIR=1, lux=35, luz apagada
│   - dormitorio: vacío
│   - pasillo: vacío
│
├─ ESCENARIO 1
│   salón ocupado + poca luz + noche
│   ──────────────────────────────────────────────
│   World model:
│   occupied = true
│   lux = 35
│   time_bucket = night
│   pref_night = 25
│
│   Planner:
│   decision = turn_on
│   brightness = 25
│
│   Acción:
│   set_room_lights("salon", on=true, brightness=25)
│
│   Resultado:
│   luz salón encendida al 25%
│
│   dormitorio y pasillo:
│   noop
│   motivo: no ocupados
│
21:02
│
├─ advance_time(+2 min)
│
├─ ESCENARIO 2
│   dormitorio ocupado + lux=10 + noche
│   ──────────────────────────────────────────────
│   salón:
│   noop
│   motivo: ya está correctamente iluminado
│
│   dormitorio:
│   occupied = true
│   lux = 10
│   pref_night = 21
│   decision = turn_on
│   brightness = 21
│
│   Acción:
│   set_room_lights("dormitorio", on=true, brightness=21)
│
│   Resultado:
│   luz dormitorio encendida al 21%
│
21:02 → 21:06
│
├─ En salón desaparece presencia
│   pir_salon = 0
│   se inicia contador absence_since = 21:02
│
21:06
│
├─ advance_time(+4 min)
│
├─ ESCENARIO 3
│   salón sigue vacío desde 21:02
│   ──────────────────────────────────────────────
│   World model:
│   occupied = false
│   absence_since = 21:02
│   now = 21:06
│
│   Planner:
│   decision = turn_off
│   motivo: ausencia sostenida durante ventana configurada
│
│   Acción:
│   set_room_lights("salon", on=false)
│
│   Resultado:
│   salón apagado
│
│   dormitorio:
│   noop
│   motivo: sigue ocupado y ya está bien iluminado
│
21:06
│
├─ ESCENARIO 4
│   override manual en dormitorio
│   ──────────────────────────────────────────────
│   Usuario cambia brillo a 12
│   event = manual_override(room="dormitorio", brightness=12)
│
│   Aprendizaje:
│   pref_night dormitorio: 21  →  18
│
│   Policy engine:
│   bloquea acciones automáticas en dormitorio
│   durante ventana manual_override_window
│
│   Además:
│   salón queda bloqueado por cooldown
│   pasillo sigue noop
│
21:17
│
├─ advance_time(+11 min)
│
├─ ESCENARIO 5
│   tras la ventana de override
│   ──────────────────────────────────────────────
│   dormitorio:
│   occupied = true
│   lux = 5
│   luz actual = 12
│   pref_night aprendida = 18
│
│   Pero el agente decide:
│   noop
│   motivo: "Current lighting already matches context"
│
│   Interpretación:
│   aunque la preferencia aprendida es 18,
│   el estado manual actual (12) no se corrige agresivamente;
│   el sistema prioriza estabilidad/no intrusión.
│
└─ Estado final
    - salón: apagado
    - dormitorio: encendido al 12%
    - pasillo: apagado
```

## 3) Diagrama por habitación

```text
SALÓN
─────
21:00   PIR=1, lux=35, luz=OFF
   ↓
Agent: turn_on @25
   ↓
21:00   luz=ON(25)

21:02   PIR=0
   ↓
absence_since = 21:02
   ↓
21:06   ausencia prolongada
   ↓
Agent: turn_off
   ↓
21:06   luz=OFF


DORMITORIO
──────────
21:02   PIR=1, lux=10, luz=OFF
   ↓
Agent: turn_on @21
   ↓
21:02   luz=ON(21)

21:06   usuario ajusta manualmente a 12
   ↓
manual_override
   ↓
aprendizaje: pref_night 21 → 18
   ↓
bloqueo temporal del agente

21:17   sigue ocupado, lux=5, luz=12
   ↓
Agent: noop
   ↓
Estado final: luz=ON(12)


PASILLO
───────
Nunca hay ocupación relevante en la demo
   ↓
Siempre noop
   ↓
Luz apagada todo el tiempo
```

## 4) Qué demuestra realmente esta salida

```text
                 DEMOSTRACIÓN DE CAPACIDADES
┌────────────────────────────────────────────────────────────┐
│ 1. Generalización por MCP                                 │
│    El agente no conoce hardware concreto.                 │
│    Solo usa tools descubiertas dinámicamente.             │
├────────────────────────────────────────────────────────────┤
│ 2. Razonamiento contextual por habitación                 │
│    Decide distinto en salón, dormitorio y pasillo.        │
├────────────────────────────────────────────────────────────┤
│ 3. Histéresis temporal                                    │
│    No apaga instantáneamente al perder presencia.         │
├────────────────────────────────────────────────────────────┤
│ 4. Respeto al humano                                      │
│    Un override manual bloquea automatización temporal.    │
├────────────────────────────────────────────────────────────┤
│ 5. Aprendizaje simple                                     │
│    Ajusta preferencia nocturna de dormitorio: 21 → 18.    │
├────────────────────────────────────────────────────────────┤
│ 6. Estabilidad                                             │
│    Evita sobrecorregir tras intervención humana.          │
└────────────────────────────────────────────────────────────┘
```

## 5) Lectura conceptual final

El comportamiento completo puede resumirse así:

```text
SENSORES ──> WORLD MODEL ──> POLICY ──> PLAN ──> ACCIÓN ──> EVENTO
   ▲                                                           │
   │                                                           ▼
   └────────────── FEEDBACK HUMANO <── APRENDIZAJE <───────────┘
```

Y en esta demo concreta:

```text
presencia + poca luz + noche  → encender tenue
ausencia sostenida            → apagar
ajuste manual del usuario     → aprender + no molestar
```
