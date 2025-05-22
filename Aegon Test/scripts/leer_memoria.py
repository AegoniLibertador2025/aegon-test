import json

def leer_memoria(clave, archivo="memoria.json"):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
        valor = datos.get(clave)
        if valor is None:
            print(f"[⚠️] La clave '{clave}' no fue encontrada.")
        else:
            print(f"[🧠] {clave} = {valor}")
        return valor
    except FileNotFoundError:
        print("[🚫] memoria.json no existe.")
        return None

# Ejemplo de uso directo
if __name__ == "__main__":
    leer_memoria("proyecto")
