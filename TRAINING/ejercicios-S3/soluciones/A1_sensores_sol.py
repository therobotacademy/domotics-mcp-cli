# Solución — Ejercicio A-1

sensores = {
    "pir_salon": {"value": 1,    "unit": "bool"},
    "lux_salon": {"value": 35.0, "unit": "lux"},
}

for nombre, datos in sensores.items():
    if nombre.startswith("pir_"):
        print(f"PIR encontrado: {nombre}  → valor {datos['value']}")
    elif nombre.startswith("lux_"):
        print(f"LUX encontrado: {nombre}  → valor {datos['value']}")
