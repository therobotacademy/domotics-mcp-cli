```
=== Tools descubiertas ===
[
  "list_tools",
  "describe_home",
  "get_room_state",
  "read_sensor",
  "get_device_state",
  "set_light",
  "set_room_lights",
  "report_manual_override",
  "set_sensor_value",
  "advance_time"
]=== Casa ===
{
  "now": "2026-03-08T21:00:00",
  "rooms": [
    {
      "room_id": "salon",
      "sensors": [
        "pir_salon",
        "lux_salon"
      ],
      "actuators": [
        "light_salon_main"
      ],
      "capabilities": [
        "dimmable_light"
      ]
    },
    {
      "room_id": "dormitorio",
      "sensors": [
        "pir_bedroom",
        "lux_bedroom"
      ],
      "actuators": [
        "light_bedroom_main"
      ],
      "capabilities": [
        "dimmable_light"
      ]
    },
    {
      "room_id": "pasillo",
      "sensors": [
        "pir_hall",
        "lux_hall"
      ],
      "actuators": [
        "light_hall"
      ],
      "capabilities": [
        "dimmable_light"
      ]
    }
  ]
}=== Escenario 1 - antes ===
{
  "room_id": "salon",
  "now": "2026-03-08T21:00:00",
  "sensors": {
    "pir_salon": {
      "value": 1,
      "unit": "bool"
    },
    "lux_salon": {
      "value": 35,
      "unit": "lux"
    }
  },
  "devices": {
    "light_salon_main": {
      "is_on": false,
      "brightness": 0
    }
  },
  "meta": {
    "last_manual_override_ts": null,
    "last_action_ts": null,
    "absence_since_ts": null
  }
}=== Escenario 1 - decisión agente ===
[
  {
    "room_id": "salon",
    "status": "executed",
    "world": {
      "room_id": "salon",
      "occupied": true,
      "occupied_confidence": 0.9,
      "lux": 35.0,
      "time_bucket": "night",
      "light_state": {
        "is_on": false,
        "brightness": 0
      },
      "preferred_brightness": {
        "morning": 60,
        "afternoon": 70,
        "night": 25
      },
      "last_manual_override_ts": null,
      "last_action_ts": null,
      "absence_since_ts": null,
      "now": "2026-03-08T21:00:00"
    },
    "plan": {
      "room_id": "salon",
      "decision": "turn_on",
      "reason": "Presence detected with low ambient light (35.0 lux).",
      "actions": [
        {
          "tool": "set_room_lights",
          "args": {
            "room_id": "salon",
            "on": true,
            "brightness": 25
          }
        }
      ]
    },
    "results": [
      {
        "ok": true,
        "room_id": "salon",
        "results": [
          {
            "ok": true,
            "room_id": "salon",
            "device_id": "light_salon_main",
            "state": {
              "is_on": true,
              "brightness": 25
            }
          }
        ]
      }
    ]
  },
  {
    "room_id": "dormitorio",
    "status": "noop",
    "world": {
      "room_id": "dormitorio",
      "occupied": false,
      "occupied_confidence": 0.1,
      "lux": 60.0,
      "time_bucket": "night",
      "light_state": {
        "is_on": false,
        "brightness": 0
      },
      "preferred_brightness": {
        "morning": 60,
        "afternoon": 70,
        "night": 21
      },
      "last_manual_override_ts": null,
      "last_action_ts": null,
      "absence_since_ts": null,
      "now": "2026-03-08T21:00:00"
    },
    "plan": {
      "room_id": "dormitorio",
      "decision": "do_nothing",
      "reason": "Room is unoccupied but absence delay has not elapsed yet.",
      "actions": []
    },
    "results": []
  },
  {
    "room_id": "pasillo",
    "status": "noop",
    "world": {
      "room_id": "pasillo",
      "occupied": false,
      "occupied_confidence": 0.1,
      "lux": 25.0,
      "time_bucket": "night",
      "light_state": {
        "is_on": false,
        "brightness": 0
      },
      "preferred_brightness": {
        "morning": 60,
        "afternoon": 70,
        "night": 25
      },
      "last_manual_override_ts": null,
      "last_action_ts": null,
      "absence_since_ts": null,
      "now": "2026-03-08T21:00:00"
    },
    "plan": {
      "room_id": "pasillo",
      "decision": "do_nothing",
      "reason": "Room is unoccupied but absence delay has not elapsed yet.",
      "actions": []
    },
    "results": []
  }
]=== Escenario 1 - después ===
{
  "room_id": "salon",
  "now": "2026-03-08T21:00:00",
  "sensors": {
    "pir_salon": {
      "value": 1,
      "unit": "bool"
    },
    "lux_salon": {
      "value": 35,
      "unit": "lux"
    }
  },
  "devices": {
    "light_salon_main": {
      "is_on": true,
      "brightness": 25
    }
  },
  "meta": {
    "last_manual_override_ts": null,
    "last_action_ts": "2026-03-08T21:00:00",
    "absence_since_ts": null
  }
}=== Escenario 2 - decisión agente ===
[
  {
    "room_id": "salon",
    "status": "noop",
    "world": {
      "room_id": "salon",
      "occupied": true,
      "occupied_confidence": 0.9,
      "lux": 35.0,
      "time_bucket": "night",
      "light_state": {
        "is_on": true,
        "brightness": 25
      },
      "preferred_brightness": {
        "morning": 60,
        "afternoon": 70,
        "night": 25
      },
      "last_manual_override_ts": null,
      "last_action_ts": "2026-03-08T21:00:00",
      "absence_since_ts": null,
      "now": "2026-03-08T21:02:00"
    },
    "plan": {
      "room_id": "salon",
      "decision": "do_nothing",
      "reason": "Current lighting already matches context.",
      "actions": []
    },
    "results": []
  },
  {
    "room_id": "dormitorio",
    "status": "executed",
    "world": {
      "room_id": "dormitorio",
      "occupied": true,
      "occupied_confidence": 0.9,
      "lux": 10.0,
      "time_bucket": "night",
      "light_state": {
        "is_on": false,
        "brightness": 0
      },
      "preferred_brightness": {
        "morning": 60,
        "afternoon": 70,
        "night": 21
      },
      "last_manual_override_ts": null,
      "last_action_ts": null,
      "absence_since_ts": null,
      "now": "2026-03-08T21:02:00"
    },
    "plan": {
      "room_id": "dormitorio",
      "decision": "turn_on",
      "reason": "Presence detected with low ambient light (10.0 lux).",
      "actions": [
        {
          "tool": "set_room_lights",
          "args": {
            "room_id": "dormitorio",
            "on": true,
            "brightness": 21
          }
        }
      ]
    },
    "results": [
      {
        "ok": true,
        "room_id": "dormitorio",
        "results": [
          {
            "ok": true,
            "room_id": "dormitorio",
            "device_id": "light_bedroom_main",
            "state": {
              "is_on": true,
              "brightness": 21
            }
          }
        ]
      }
    ]
  },
  {
    "room_id": "pasillo",
    "status": "noop",
    "world": {
      "room_id": "pasillo",
      "occupied": false,
      "occupied_confidence": 0.1,
      "lux": 25.0,
      "time_bucket": "night",
      "light_state": {
        "is_on": false,
        "brightness": 0
      },
      "preferred_brightness": {
        "morning": 60,
        "afternoon": 70,
        "night": 25
      },
      "last_manual_override_ts": null,
      "last_action_ts": null,
      "absence_since_ts": null,
      "now": "2026-03-08T21:02:00"
    },
    "plan": {
      "room_id": "pasillo",
      "decision": "do_nothing",
      "reason": "Room is unoccupied but absence delay has not elapsed yet.",
      "actions": []
    },
    "results": []
  }
]=== Escenario 2 - dormitorio ===
{
  "room_id": "dormitorio",
  "now": "2026-03-08T21:02:00",
  "sensors": {
    "pir_bedroom": {
      "value": 1,
      "unit": "bool"
    },
    "lux_bedroom": {
      "value": 10,
      "unit": "lux"
    }
  },
  "devices": {
    "light_bedroom_main": {
      "is_on": true,
      "brightness": 21
    }
  },
  "meta": {
    "last_manual_override_ts": null,
    "last_action_ts": "2026-03-08T21:02:00",
    "absence_since_ts": null
  }
}=== Escenario 3 - decisión agente ===
[
  {
    "room_id": "salon",
    "status": "executed",
    "world": {
      "room_id": "salon",
      "occupied": false,
      "occupied_confidence": 0.1,
      "lux": 35.0,
      "time_bucket": "night",
      "light_state": {
        "is_on": true,
        "brightness": 25
      },
      "preferred_brightness": {
        "morning": 60,
        "afternoon": 70,
        "night": 25
      },
      "last_manual_override_ts": null,
      "last_action_ts": "2026-03-08T21:00:00",
      "absence_since_ts": "2026-03-08T21:02:00",
      "now": "2026-03-08T21:06:00"
    },
    "plan": {
      "room_id": "salon",
      "decision": "turn_off",
      "reason": "Room has been unoccupied for at least the configured absence window.",
      "actions": [
        {
          "tool": "set_room_lights",
          "args": {
            "room_id": "salon",
            "on": false
          }
        }
      ]
    },
    "results": [
      {
        "ok": true,
        "room_id": "salon",
        "results": [
          {
            "ok": true,
            "room_id": "salon",
            "device_id": "light_salon_main",
            "state": {
              "is_on": false,
              "brightness": 0
            }
          }
        ]
      }
    ]
  },
  {
    "room_id": "dormitorio",
    "status": "noop",
    "world": {
      "room_id": "dormitorio",
      "occupied": true,
      "occupied_confidence": 0.9,
      "lux": 10.0,
      "time_bucket": "night",
      "light_state": {
        "is_on": true,
        "brightness": 21
      },
      "preferred_brightness": {
        "morning": 60,
        "afternoon": 70,
        "night": 21
      },
      "last_manual_override_ts": null,
      "last_action_ts": "2026-03-08T21:02:00",
      "absence_since_ts": null,
      "now": "2026-03-08T21:06:00"
    },
    "plan": {
      "room_id": "dormitorio",
      "decision": "do_nothing",
      "reason": "Current lighting already matches context.",
      "actions": []
    },
    "results": []
  },
  {
    "room_id": "pasillo",
    "status": "noop",
    "world": {
      "room_id": "pasillo",
      "occupied": false,
      "occupied_confidence": 0.1,
      "lux": 25.0,
      "time_bucket": "night",
      "light_state": {
        "is_on": false,
        "brightness": 0
      },
      "preferred_brightness": {
        "morning": 60,
        "afternoon": 70,
        "night": 25
      },
      "last_manual_override_ts": null,
      "last_action_ts": null,
      "absence_since_ts": null,
      "now": "2026-03-08T21:06:00"
    },
    "plan": {
      "room_id": "pasillo",
      "decision": "do_nothing",
      "reason": "Room is unoccupied but absence delay has not elapsed yet.",
      "actions": []
    },
    "results": []
  }
]=== Escenario 3 - salón ===
{
  "room_id": "salon",
  "now": "2026-03-08T21:06:00",
  "sensors": {
    "pir_salon": {
      "value": 0,
      "unit": "bool"
    },
    "lux_salon": {
      "value": 35,
      "unit": "lux"
    }
  },
  "devices": {
    "light_salon_main": {
      "is_on": false,
      "brightness": 0
    }
  },
  "meta": {
    "last_manual_override_ts": null,
    "last_action_ts": "2026-03-08T21:06:00",
    "absence_since_ts": "2026-03-08T21:02:00"
  }
}=== Escenario 4 - preferencia aprendida ===
{
  "new_night_preference": 18
}=== Escenario 4 - agente bloqueado por override ===
[
  {
    "room_id": "salon",
    "status": "blocked",
    "policy_reason": "cooldown",
    "world": {
      "room_id": "salon",
      "occupied": false,
      "occupied_confidence": 0.1,
      "lux": 35.0,
      "time_bucket": "night",
      "light_state": {
        "is_on": false,
        "brightness": 0
      },
      "preferred_brightness": {
        "morning": 60,
        "afternoon": 70,
        "night": 25
      },
      "last_manual_override_ts": null,
      "last_action_ts": "2026-03-08T21:06:00",
      "absence_since_ts": "2026-03-08T21:02:00",
      "now": "2026-03-08T21:06:00"
    }
  },
  {
    "room_id": "dormitorio",
    "status": "blocked",
    "policy_reason": "manual_override_window",
    "world": {
      "room_id": "dormitorio",
      "occupied": true,
      "occupied_confidence": 0.9,
      "lux": 5.0,
      "time_bucket": "night",
      "light_state": {
        "is_on": true,
        "brightness": 12
      },
      "preferred_brightness": {
        "morning": 60,
        "afternoon": 70,
        "night": 18
      },
      "last_manual_override_ts": "2026-03-08T21:06:00",
      "last_action_ts": "2026-03-08T21:02:00",
      "absence_since_ts": null,
      "now": "2026-03-08T21:06:00"
    }
  },
  {
    "room_id": "pasillo",
    "status": "noop",
    "world": {
      "room_id": "pasillo",
      "occupied": false,
      "occupied_confidence": 0.1,
      "lux": 25.0,
      "time_bucket": "night",
      "light_state": {
        "is_on": false,
        "brightness": 0
      },
      "preferred_brightness": {
        "morning": 60,
        "afternoon": 70,
        "night": 25
      },
      "last_manual_override_ts": null,
      "last_action_ts": null,
      "absence_since_ts": null,
      "now": "2026-03-08T21:06:00"
    },
    "plan": {
      "room_id": "pasillo",
      "decision": "do_nothing",
      "reason": "Room is unoccupied but absence delay has not elapsed yet.",
      "actions": []
    },
    "results": []
  }
]=== Escenario 5 - agente tras override ===
[
  {
    "room_id": "salon",
    "status": "noop",
    "world": {
      "room_id": "salon",
      "occupied": false,
      "occupied_confidence": 0.1,
      "lux": 35.0,
      "time_bucket": "night",
      "light_state": {
        "is_on": false,
        "brightness": 0
      },
      "preferred_brightness": {
        "morning": 60,
        "afternoon": 70,
        "night": 25
      },
      "last_manual_override_ts": null,
      "last_action_ts": "2026-03-08T21:06:00",
      "absence_since_ts": "2026-03-08T21:02:00",
      "now": "2026-03-08T21:17:00"
    },
    "plan": {
      "room_id": "salon",
      "decision": "do_nothing",
      "reason": "Room is unoccupied but absence delay has not elapsed yet.",
      "actions": []
    },
    "results": []
  },
  {
    "room_id": "dormitorio",
    "status": "noop",
    "world": {
      "room_id": "dormitorio",
      "occupied": true,
      "occupied_confidence": 0.9,
      "lux": 5.0,
      "time_bucket": "night",
      "light_state": {
        "is_on": true,
        "brightness": 12
      },
      "preferred_brightness": {
        "morning": 60,
        "afternoon": 70,
        "night": 18
      },
      "last_manual_override_ts": "2026-03-08T21:06:00",
      "last_action_ts": "2026-03-08T21:02:00",
      "absence_since_ts": null,
      "now": "2026-03-08T21:17:00"
    },
    "plan": {
      "room_id": "dormitorio",
      "decision": "do_nothing",
      "reason": "Current lighting already matches context.",
      "actions": []
    },
    "results": []
  },
  {
    "room_id": "pasillo",
    "status": "noop",
    "world": {
      "room_id": "pasillo",
      "occupied": false,
      "occupied_confidence": 0.1,
      "lux": 25.0,
      "time_bucket": "night",
      "light_state": {
        "is_on": false,
        "brightness": 0
      },
      "preferred_brightness": {
        "morning": 60,
        "afternoon": 70,
        "night": 25
      },
      "last_manual_override_ts": null,
      "last_action_ts": null,
      "absence_since_ts": null,
      "now": "2026-03-08T21:17:00"
    },
    "plan": {
      "room_id": "pasillo",
      "decision": "do_nothing",
      "reason": "Room is unoccupied but absence delay has not elapsed yet.",
      "actions": []
    },
    "results": []
  }
]=== Estado final dormitorio ===
{
  "room_id": "dormitorio",
  "now": "2026-03-08T21:17:00",
  "sensors": {
    "pir_bedroom": {
      "value": 1,
      "unit": "bool"
    },
    "lux_bedroom": {
      "value": 5,
      "unit": "lux"
    }
  },
  "devices": {
    "light_bedroom_main": {
      "is_on": true,
      "brightness": 12
    }
  },
  "meta": {
    "last_manual_override_ts": "2026-03-08T21:06:00",
    "last_action_ts": "2026-03-08T21:02:00",
    "absence_since_ts": null
  }
}=== Eventos recientes ===
[
  {
    "ts": "2026-03-08T21:00:00",
    "kind": "sensor_update",
    "payload": {
      "room_id": "salon",
      "sensor_id": "lux_salon",
      "value": 35
    }
  },
  {
    "ts": "2026-03-08T21:00:00",
    "kind": "sensor_update",
    "payload": {
      "room_id": "salon",
      "sensor_id": "pir_salon",
      "value": 1
    }
  },
  {
    "ts": "2026-03-08T21:00:00",
    "kind": "set_light",
    "payload": {
      "room_id": "salon",
      "device_id": "light_salon_main",
      "on": true,
      "brightness": 25
    }
  },
  {
    "ts": "2026-03-08T21:02:00",
    "kind": "time_advanced",
    "payload": {
      "minutes": 2,
      "now": "2026-03-08T21:02:00"
    }
  },
  {
    "ts": "2026-03-08T21:02:00",
    "kind": "sensor_update",
    "payload": {
      "room_id": "dormitorio",
      "sensor_id": "lux_bedroom",
      "value": 10
    }
  },
  {
    "ts": "2026-03-08T21:02:00",
    "kind": "sensor_update",
    "payload": {
      "room_id": "dormitorio",
      "sensor_id": "pir_bedroom",
      "value": 1
    }
  },
  {
    "ts": "2026-03-08T21:02:00",
    "kind": "set_light",
    "payload": {
      "room_id": "dormitorio",
      "device_id": "light_bedroom_main",
      "on": true,
      "brightness": 21
    }
  },
  {
    "ts": "2026-03-08T21:02:00",
    "kind": "sensor_update",
    "payload": {
      "room_id": "salon",
      "sensor_id": "pir_salon",
      "value": 0
    }
  },
  {
    "ts": "2026-03-08T21:06:00",
    "kind": "time_advanced",
    "payload": {
      "minutes": 4,
      "now": "2026-03-08T21:06:00"
    }
  },
  {
    "ts": "2026-03-08T21:06:00",
    "kind": "set_light",
    "payload": {
      "room_id": "salon",
      "device_id": "light_salon_main",
      "on": false,
      "brightness": 0
    }
  },
  {
    "ts": "2026-03-08T21:06:00",
    "kind": "manual_override",
    "payload": {
      "room_id": "dormitorio",
      "brightness": 12,
      "source": "wall_switch"
    }
  },
  {
    "ts": "2026-03-08T21:06:00",
    "kind": "sensor_update",
    "payload": {
      "room_id": "dormitorio",
      "sensor_id": "pir_bedroom",
      "value": 1
    }
  },
  {
    "ts": "2026-03-08T21:06:00",
    "kind": "sensor_update",
    "payload": {
      "room_id": "dormitorio",
      "sensor_id": "lux_bedroom",
      "value": 5
    }
  },
  {
    "ts": "2026-03-08T21:17:00",
    "kind": "time_advanced",
    "payload": {
      "minutes": 11,
      "now": "2026-03-08T21:17:00"
    }
  }
]
```
