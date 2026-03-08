Funcionalmente, el código implementa una idea muy concreta:  **el agente no controla hardware directamente** . En lugar de eso, trabaja contra una **superficie MCP-like** que le expone capacidades de la casa como tools. Esa separación es lo más importante del diseño.

## Visión general

La PoC está dividida en dos bloques:

```text
1) Servidor MCP-like
   Expone tools estandarizadas:
   leer sensores, leer estado, actuar sobre luces, registrar override, avanzar tiempo.

2) Agente
   Descubre tools, construye su modelo del mundo, aplica política,
   planifica, ejecuta acciones y aprende preferencias.
```

La idea fuerte es esta:

```text
[Casa / simulador / hardware real]
            ↓
   [Servidor MCP-like]
            ↓
        [Agente]
```

Eso hace que el agente sea  **portable** . Si mañana cambias el backend por ESP32, Home Assistant o Zigbee2MQTT, el agente apenas cambia, porque su interfaz sigue siendo MCP.

## 1. Qué papel juega MCP en esta PoC

Aquí MCP no aparece como librería oficial, sino como  **patrón arquitectónico** . El servidor implementa una interfaz de tools accesible por HTTP que cumple la función de un MCP server:

* publica qué herramientas existen,
* describe el entorno,
* permite invocar tools por nombre y argumentos,
* desacopla razonamiento y hardware.

En otras palabras, el servidor MCP-like convierte la casa en un  **espacio de capacidades discoverable** .

### Qué tools expone

El servidor anuncia este catálogo:

```text
list_tools
describe_home
get_room_state
read_sensor
get_device_state
set_light
set_room_lights
report_manual_override
set_sensor_value
advance_time
```

Estas tools cumplen tres funciones distintas.

Primero,  **descubrimiento** :

* `list_tools`
* `describe_home`

Segundo,  **observación del entorno** :

* `get_room_state`
* `read_sensor`
* `get_device_state`

Tercero,  **acción y simulación** :

* `set_light`
* `set_room_lights`
* `report_manual_override`
* `set_sensor_value`
* `advance_time`

Eso es clave: el agente no “sabe” que hay un PIR real conectado a un pin GPIO. Solo sabe que existe una tool con la que puede leer presencia o encender una luz.

## 2. Cómo está construido el servidor MCP-like

El núcleo está en `mcp_server/server.py`.

### Estado global de la casa

El servidor mantiene un `STATE` con:

* hora actual,
* habitaciones,
* sensores,
* dispositivos,
* metadatos,
* eventos.

Cada habitación tiene una estructura de este estilo:

```text
room
 ├─ sensors
 │   ├─ PIR
 │   └─ lux
 ├─ devices
 │   └─ luz regulable
 └─ meta
     ├─ last_manual_override_ts
     ├─ last_action_ts
     └─ absence_since_ts
```

Esto importa mucho para el agente, porque los metadatos no son simple telemetría: son **memoria operativa** del sistema.

### Endpoints principales

`/list_tools`
devuelve el catálogo de herramientas disponibles. Desde la perspectiva MCP, esto permite al agente **descubrir dinámicamente las affordances** del entorno.

`/describe_home`
devuelve la topología semántica de la casa:

* habitaciones,
* sensores por habitación,
* actuadores por habitación,
* capacidades.

Esto le permite al agente pensar en términos de  **rooms, sensors, actuators** , no en hardware específico.

`/get_room_state/{room_id}`
devuelve el snapshot completo de una habitación:

* valores de sensores,
* estado de dispositivos,
* metadatos temporales.

Este endpoint es fundamental porque el agente puede reconstruir el contexto completo de cada habitación sin hacer múltiples lecturas sueltas.

`/call_tool`
es el despacho central. Recibe:

* `tool`
* `args`

y enruta a la implementación concreta. Esta parte es la esencia MCP-like: el agente invoca capacidades  **por nombre** , no por función local ni por dependencia hardware.

### Tools de acción

`_set_light()` y `_set_room_lights()`
cambian el estado de las luces y actualizan `last_action_ts`. Además registran un evento `set_light`.

Esto es importante porque el agente no solo actúa: también deja trazabilidad y activa mecanismos posteriores como cooldown.

`_report_manual_override()`
simula una intervención humana. Marca `last_manual_override_ts` y opcionalmente actualiza el brillo real del dispositivo.

Arquitectónicamente, esta tool es crucial: introduce una **fuente de autoridad humana** distinta del agente.

`_set_sensor_value()`
simula entradas del entorno. Si el sensor es PIR y pasa a 0, se inicia `absence_since_ts`. Si vuelve a 1, se limpia esa marca.

Este pequeño detalle implementa la histéresis temporal: no basta “no hay presencia ahora”; importa desde cuándo no la hay.

`_advance_time()`
avanza el reloj del simulador. Sirve para probar el comportamiento temporal del agente sin esperar en tiempo real.

## 3. Cómo funciona el agente

El núcleo está en `agent/agent.py`.

La clase importante es `LightingAgent`. Su trabajo no es “encender luces”, sino recorrer este pipeline:

```text
discover → inspect → build world → apply policy → plan → execute → log
```

### 3.1 MCPClient

`MCPClient` encapsula el acceso al servidor. Tiene cuatro funciones conceptualmente muy limpias:

* `list_tools()`
* `describe_home()`
* `get_room_state(room_id)`
* `call_tool(tool, args)`

Este cliente ya muestra el principio de diseño: el agente solo conoce una  **API de capacidades** . No importa si detrás hay FastAPI, un microcontrolador o Home Assistant.

### 3.2 discover_tools()

Aquí el agente llama a `list_tools()` y guarda el resultado en `tool_registry`.

Funcionalmente, esta parte hace dos cosas:

* valida qué puede hacer el sistema,
* evita acoplar el agente a un conjunto fijo de acciones hardcodeadas.

En esta PoC el executor soporta solo ciertas tools, pero el diseño ya está preparado para una evolución donde el planner sea más dinámico.

### 3.3 inspect_home()

Llama a `describe_home()` y obtiene el mapa de habitaciones. Gracias a esto el agente puede iterar sobre la casa como una colección de espacios con capacidades.

No está recorriendo “dispositivos IP”; está recorriendo un  **modelo del entorno** .

### 3.4 process_once()

Éste es el corazón funcional del agente.

Su lógica real es:

```text
para cada habitación:
    1. leer estado bruto
    2. cargar preferencias
    3. construir estado semántico (world model)
    4. aplicar política dura
    5. si se permite, generar plan
    6. ejecutar acciones si las hay
    7. registrar todo
```

Eso ya es un agente, aunque el planner sea heurístico y no LLM.

## 4. El world model: donde el agente deja de ver hardware

Esto ocurre en `agent/world_model.py`.

El servidor devuelve un snapshot “físico”:

* `pir_bedroom = 1`
* `lux_bedroom = 10`
* `light_bedroom_main = {is_on: false, brightness: 0}`

El agente lo transforma en una representación más cognitiva:

* `occupied = true`
* `occupied_confidence = 0.9`
* `lux = 10`
* `time_bucket = night`
* `preferred_brightness = {...}`
* `last_manual_override_ts = ...`
* `absence_since_ts = ...`

Éste es el punto donde el sistema pasa de ser domótica clásica a arquitectura agente.

### Por qué importa este paso

Porque el agente no razona sobre:

* pines,
* payloads eléctricos,
* endpoints concretos.

Razona sobre conceptos:

* ocupación,
* luminosidad,
* franja horaria,
* intención de confort,
* intervención humana reciente.

Ese desacoplamiento semántico es exactamente lo que necesitas si quieres que el agente generalice a “cualquier sistema”.

## 5. La policy: la parte no negociable del sistema

Esto está en `agent/policy.py`.

Aquí hay una decisión arquitectónica muy buena:  **la política dura no se delega al planner** .

La función `apply_policy(room_state)` bloquea acción si ocurre alguna de estas situaciones:

* hay un `manual_override` reciente,
* hay `cooldown` tras una acción reciente.

Eso significa que el agente no es totalmente libre. Está encapsulado dentro de guardarraíles deterministas.

### Por qué esto es tan importante

En un sistema domótico real, el agente no debería tener la última palabra en todo. Debe existir una capa que impida comportamientos molestos o peligrosos.

En esta PoC, la policy introduce tres ideas muy valiosas:

#### 1. Respeto al usuario

Si el usuario intervino manualmente hace menos de 10 minutos, el agente se bloquea.

#### 2. Estabilidad

Si el agente actuó hace menos de 60 segundos, no vuelve a tocar esa habitación.

#### 3. Histéresis temporal

La función `should_turn_off_after_absence()` comprueba si la ausencia dura al menos 3 minutos.

Esto evita el típico comportamiento torpe de sistemas rígidos que apagan por un falso negativo instantáneo.

### clamp_brightness()

Otra política importante: de noche, el brillo máximo se limita a 30.

Eso significa que incluso si una preferencia aprendida fuese alta, la policy sigue imponiendo una restricción contextual.

De nuevo:  **el agente propone dentro de límites** , no manda sin control.

## 6. El planner: el “cerebro” actual del agente

Está en `agent/planner.py`.

Aquí no hay LLM todavía. Hay un planificador heurístico, pero está estructurado como si más adelante fuese a sustituirse por uno basado en modelo.

Eso está muy bien hecho.

### Qué hace el planner

Recibe `room_state` y decide una de tres cosas:

* `turn_on`
* `turn_off`
* `do_nothing`

Y genera un plan estructurado:

```json
{
  "room_id": "...",
  "decision": "...",
  "reason": "...",
  "actions": [...]
}
```

Eso es importante: el planner no ejecuta. Solo produce una  **intención accionable** .

### Lógica del planner

#### Caso 1: habitación no ocupada

Si la luz está encendida y la ausencia ha durado suficiente, decide apagar.

Si no ha pasado suficiente tiempo, hace `do_nothing`.

Aquí se ve claramente la cooperación entre planner y policy:

* la policy controla ventanas duras,
* el planner decide la acción contextual.

#### Caso 2: mucha luz ambiental

Si `lux >= 200` y la luz está encendida, decide apagar.

#### Caso 3: poca luz ambiental

Si `lux < 80`, calcula un brillo objetivo desde las preferencias y la policy nocturna.

Si la luz está apagada, o el brillo actual difiere mucho del objetivo, decide encender/ajustar.

#### Caso 4: contexto ya satisfecho

No toca nada.

### Aspecto agente relevante

El planner trabaja con:

* estado,
* preferencias,
* contexto temporal,
* restricciones derivadas.

Eso lo acerca a un agente deliberativo muy simple:

* **percibe**
* **interpreta**
* **elige una intención**
* **expresa un plan**

## 7. El executor: dónde el plan se convierte en acción MCP

Está en `agent/executor.py`.

Su trabajo es muy simple y precisamente por eso es correcto:

* toma el plan,
* recorre `actions`,
* verifica que la tool esté soportada,
* invoca `mcp_client.call_tool(...)`.

### Por qué esta simplicidad es buena

Porque separa muy bien responsabilidades:

* el planner decide,
* el executor actúa,
* el MCP server materializa.

Si mañana cambias el planner por un LLM, el executor puede seguir igual.

Además, al filtrar tools soportadas, el executor actúa como una segunda barrera de seguridad.

## 8. Aprendizaje: el agente modifica sus preferencias, no las reglas del mundo

Esto está en `agent/preferences.py` y en `learn_from_manual_override()` de `agent.py`.

### PreferenceStore

Guarda en SQLite preferencias por:

* habitación,
* franja horaria.

La tabla es:

```text
(room_id, time_bucket) -> brightness
```

### Qué representa esto funcionalmente

No es aprendizaje complejo. Es aprendizaje de bajo coste y alta interpretabilidad:

* el usuario ajusta manualmente,
* el sistema interpreta ese ajuste como señal de preferencia,
* la próxima vez el planner parte de un brillo más cercano.

Eso tiene varias ventajas:

* no hace falta entrenamiento pesado,
* se entiende fácilmente,
* se puede inspeccionar y corregir.

### update_preference()

La actualización usa una media suavizada. El sistema no sustituye bruscamente el valor previo por el nuevo. Lo desplaza progresivamente.

Eso evita sobreajustar por una sola acción aislada del usuario.

### learn_from_manual_override()

Cuando se detecta un override manual, el agente:

1. relee el estado de la habitación,
2. obtiene la franja horaria,
3. actualiza la preferencia para esa franja,
4. deja log del aprendizaje.

Eso convierte una intervención humana en una señal semántica, no solo en un cambio de estado puntual.

## 9. El script de demo: cómo se demuestra el comportamiento agente + MCP

Está en `run_demo.py`.

Este script hace de laboratorio reproducible. No es parte del núcleo lógico, pero sí muestra muy bien la arquitectura.

### Qué hace

Primero resetea el servidor.

Después crea el agente y ejecuta:

1. descubrimiento de tools,
2. inspección de la casa,
3. alteración de sensores usando tools MCP,
4. invocación del ciclo del agente,
5. observación del estado resultante.

Esto es importante: incluso para preparar escenarios, el script usa tools del servidor, no accede a estructuras internas del simulador. Eso preserva la idea MCP.

### Escenarios

#### Escenario 1

Salón con presencia y baja luz nocturna.
El agente enciende al brillo nocturno preferido.

#### Escenario 2

Dormitorio con presencia y muy baja luz.
El agente enciende con brillo adaptado.

#### Escenario 3

Ausencia sostenida en salón.
El agente apaga tras la ventana temporal.

#### Escenario 4

Override manual en dormitorio.
El agente aprende una nueva preferencia y queda bloqueado temporalmente.

#### Escenario 5

Tras pasar el tiempo, el agente vuelve a operar, pero sin corregir agresivamente el ajuste humano.

Eso último es muy valioso: el sistema no solo aprende, también evita ser intrusivo.

## 10. Qué demuestra esta PoC sobre Agentes

Desde el punto de vista de arquitectura de agentes, el proyecto demuestra cinco cosas.

### 1. Un agente no necesita tocar hardware directamente

La capa MCP abstrae sensores y actuadores como tools.

### 2. El agente necesita un modelo del mundo

No basta con leer sensores sueltos. Hay que construir una representación semántica.

### 3. La autonomía debe estar acotada por policy

La inteligencia sin guardarraíles en domótica suele terminar en oscilaciones o decisiones molestas.

### 4. La acción debe salir en formato estructurado

El planner produce planes explícitos y el executor los materializa.

### 5. El aprendizaje útil en domótica puede ser muy simple

No hace falta RL complejo para obtener adaptación real. Basta con incorporar feedback humano de forma incremental.

## 11. Qué demuestra esta PoC sobre MCP

Desde el punto de vista MCP, la lección principal es muy clara:

**MCP convierte la casa en un espacio uniforme de capacidades.**

Eso habilita tres propiedades muy potentes.

### Descubrimiento

El agente puede empezar preguntando “qué tools existen”.

### Portabilidad

El agente no depende del hardware concreto.

### Orquestación

El agente puede combinar percepción, acción y aprendizaje a través de una interfaz homogénea.

En una implementación futura más fiel al estándar MCP, podrías tener:

* tools remotas,
* resources,
* prompts,
* streaming,
* múltiples servidores MCP especializados.

Pero la idea arquitectónica ya está aquí.

## 12. Lectura final del código en una sola imagen mental

```text
MCP Server
   ├─ publica tools
   ├─ describe la casa
   ├─ da estado y sensores
   ├─ ejecuta acciones
   └─ registra eventos

LightingAgent
   ├─ descubre tools
   ├─ inspecciona habitaciones
   ├─ construye world model
   ├─ aplica policy
   ├─ genera plan
   ├─ ejecuta vía MCP
   └─ aprende preferencias

Resultado
   ├─ control contextual
   ├─ respeto al override humano
   ├─ histéresis temporal
   ├─ aprendizaje simple
   └─ independencia del hardware
```

## 13. Valor didáctico real del diseño

Como PoC docente, el código está bien planteado porque permite explicar por separado:

* qué es una tool,
* qué es un servidor MCP,
* qué hace un agente más allá de “llamar a un modelo”,
* por qué conviene separar world model, policy, planner y executor,
* cómo introducir aprendizaje sin complicar el sistema.

Dicho de forma simple: no es solo una demo de luces; es una demo de  **cómo envolver un sistema físico con una arquitectura agente modular** .
