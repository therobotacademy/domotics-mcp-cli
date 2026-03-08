# DEMO AGENTE DOMÓTICO VÍA MCP

## Iluminación inteligente por habitaciones

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                          DEMO: AGENTE INTELIGENTE + MCP + ILUMINACIÓN                       │
│──────────────────────────────────────────────────────────────────────────────────────────────│
│ IDEA CLAVE                                                                                    │
│ El agente NO conoce el hardware.                                                             │
│ Solo descubre tools MCP, construye un modelo del hogar y decide qué hacer en cada habitación│
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

```text
┌──────────────────────────────┐       ┌──────────────────────────────┐       ┌──────────────────────────────┐
│     1) MCP SERVER / CASA     │ ───►  │      2) WORLD MODEL         │ ───►  │      3) POLICY ENGINE       │
│──────────────────────────────│       │──────────────────────────────│       │──────────────────────────────│
│ Tools descubiertas           │       │ Estado por habitación        │       │ Reglas de seguridad         │
│                              │       │                              │       │                              │
│ • list_tools                 │       │ • occupied                   │       │ • cooldown                   │
│ • describe_home              │       │ • lux                        │       │ • manual override window     │
│ • get_room_state             │       │ • time_bucket = night        │       │ • ventana de ausencia        │
│ • read_sensor                │       │ • light_state                │       │                              │
│ • get_device_state           │       │ • preferencias               │       │ Decide si:                   │
│ • set_light                  │       │ • meta temporal              │       │ • bloquear                   │
│ • set_room_lights            │       │                              │       │ • permitir                   │
│ • report_manual_override     │       └──────────────────────────────┘       │ • no actuar                  │
│ • set_sensor_value           │                                              └──────────────────────────────┘
│ • advance_time               │
└──────────────────────────────┘
                                                                         │
                                                                         ▼
                                              ┌────────────────────────────────────────────┐
                                              │         4) PLANNER + EXECUTOR             │
                                              │────────────────────────────────────────────│
                                              │ Planifica y ejecuta acciones MCP          │
                                              │                                            │
                                              │ • turn_on                                 │
                                              │ • turn_off                                │
                                              │ • do_nothing                              │
                                              │                                            │
                                              │ Ejemplo:                                  │
                                              │ set_room_lights("salon", on=true, 25)     │
                                              └────────────────────────────────────────────┘
                                                                         │
                                                                         ▼
                                              ┌────────────────────────────────────────────┐
                                              │       5) FEEDBACK + APRENDIZAJE            │
                                              │────────────────────────────────────────────│
                                              │ Si el usuario corrige manualmente:         │
                                              │ • el agente aprende preferencia            │
                                              │ • se bloquea temporalmente                 │
                                              └────────────────────────────────────────────┘
```

## Flujo temporal de la demo

```text
21:00
│
├── ESCENARIO 1: SALÓN
│   Sensores:
│   • presencia = 1
│   • lux = 35
│   • luz = apagada
│
│   Interpretación:
│   • habitación ocupada
│   • poca luz
│   • franja = night
│
│   Decisión del agente:
│   • turn_on
│   • brightness = 25
│
│   Resultado:
│   • salón encendido al 25%
│
└────────────────────────────────────────────────────────────────────────────────────────────

21:02
│
├── ESCENARIO 2: DORMITORIO
│   Sensores:
│   • presencia = 1
│   • lux = 10
│   • luz = apagada
│
│   Interpretación:
│   • ocupación confirmada
│   • muy poca luz
│   • franja = night
│
│   Decisión del agente:
│   • turn_on
│   • brightness = 21
│
│   Resultado:
│   • dormitorio encendido al 21%
│
│   Salón:
│   • noop
│   • ya estaba correctamente ajustado
│
└────────────────────────────────────────────────────────────────────────────────────────────

21:02 → 21:06
│
├── ESCENARIO 3: AUSENCIA EN SALÓN
│   Evento:
│   • el PIR del salón pasa a 0
│   • se inicia temporizador de ausencia
│
│   A las 21:06:
│   • la ausencia ya dura lo suficiente
│
│   Decisión del agente:
│   • turn_off
│
│   Resultado:
│   • salón apagado
│
└────────────────────────────────────────────────────────────────────────────────────────────

21:06
│
├── ESCENARIO 4: OVERRIDE MANUAL EN DORMITORIO
│   Evento humano:
│   • el usuario cambia el brillo a 12
│   • source = wall_switch
│
│   Efecto 1: aprendizaje
│   • preferencia noche: 21 → 18
│
│   Efecto 2: protección
│   • el agente entra en manual_override_window
│   • no contradice inmediatamente al usuario
│
│   Además:
│   • salón queda bloqueado por cooldown
│
└────────────────────────────────────────────────────────────────────────────────────────────

21:17
│
├── ESCENARIO 5: TRAS LA VENTANA DE OVERRIDE
│   Dormitorio:
│   • presencia = 1
│   • lux = 5
│   • luz actual = 12
│   • preferencia aprendida = 18
│
│   Decisión del agente:
│   • noop
│
│   Lectura:
│   • el sistema prioriza estabilidad
│   • no sobrecorrige tras intervención humana
│
│   Estado final:
│   • salón = apagado
│   • dormitorio = encendido al 12%
│   • pasillo = apagado
│
└────────────────────────────────────────────────────────────────────────────────────────────
```

## Resumen visual por habitación

```text
┌───────────────────────┬──────────────────────────────────────────────┬─────────────────────────────┐
│ HABITACIÓN            │ SECUENCIA                                    │ RESULTADO                   │
├───────────────────────┼──────────────────────────────────────────────┼─────────────────────────────┤
│ SALÓN                 │ 21:00 presencia + lux bajo  → encender 25    │ ON 25%                      │
│                       │ 21:02 pierde presencia                        │ temporizador ausencia       │
│                       │ 21:06 ausencia sostenida → apagar             │ OFF                         │
├───────────────────────┼──────────────────────────────────────────────┼─────────────────────────────┤
│ DORMITORIO            │ 21:02 presencia + lux bajo → encender 21     │ ON 21%                      │
│                       │ 21:06 usuario ajusta a 12                     │ aprendizaje 21 → 18         │
│                       │ 21:06 override bloquea agente temporalmente   │ respeto al usuario          │
│                       │ 21:17 agente no corrige                       │ ON 12%                      │
├───────────────────────┼──────────────────────────────────────────────┼─────────────────────────────┤
│ PASILLO               │ sin presencia relevante                       │ siempre noop / OFF          │
└───────────────────────┴──────────────────────────────────────────────┴─────────────────────────────┘
```

## Qué demuestra esta PoC

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   CAPACIDADES DEMOSTRADAS                                   │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. Abstracción MCP                                                                          │
│    El agente opera con tools genéricas, no con hardware específico.                        │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. Razonamiento contextual                                                                  │
│    Decide distinto según habitación, ocupación, lux y franja horaria.                      │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│ 3. Histéresis temporal                                                                      │
│    No apaga instantáneamente al perder presencia.                                           │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│ 4. Respeto de la intervención humana                                                        │
│    Un override manual bloquea la automatización durante una ventana temporal.               │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│ 5. Aprendizaje incremental                                                                  │
│    El sistema ajusta la preferencia nocturna del dormitorio: 21 → 18.                      │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│ 6. Estabilidad                                                                              │
│    El agente evita sobre-actuar y mantiene una experiencia no intrusiva.                   │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Mensaje final de la slide

```text
SENSORES ──► WORLD MODEL ──► POLICY ──► PLAN ──► ACCIÓN ──► EVENTOS
    ▲                                                           │
    └──────────────── FEEDBACK HUMANO ◄── APRENDIZAJE ◄─────────┘
```

```text
presencia + poca luz + noche   → encender tenue
ausencia sostenida             → apagar
ajuste manual del usuario      → aprender + no molestar
```

Puedo convertir esta misma infografía en una **diapositiva PowerPoint editable** con formato visual docente.
