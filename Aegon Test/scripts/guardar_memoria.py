import json

def guardar_memoria(clave, valor, archivo="memoria.json"):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except FileNotFoundError:
        datos = {}

    datos[clave] = valor

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2)

    print(f"[🧠] Guardado: {clave} = {valor}")

# Ejemplo de uso directo
if __name__ == "__main__":
    guardar_memoria("proyecto", "aegon_web")
