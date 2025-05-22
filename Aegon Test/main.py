from flask import Flask, request, jsonify
import os
import json
import subprocess

app = Flask(__name__)

MEMORIA_PATH = "memoria.json"
SCRIPTS_DIR = "scripts"

# Asegurar existencia de carpeta de scripts y memoria
os.makedirs(SCRIPTS_DIR, exist_ok=True)
if not os.path.exists(MEMORIA_PATH):
    with open(MEMORIA_PATH, "w", encoding="utf-8") as f:
        json.dump({}, f)

@app.route("/")
def home():
    return "✅ AEGON está en línea con memoria y control de scripts."

# -------- MEMORIA --------
@app.route("/guardar_memoria", methods=["POST"])
def guardar_memoria():
    data = request.json
    clave = data.get("clave")
    valor = data.get("valor")

    with open(MEMORIA_PATH, "r+", encoding="utf-8") as f:
        memoria = json.load(f)
        memoria[clave] = valor
        f.seek(0)
        json.dump(memoria, f, indent=2)
        f.truncate()
    
    return jsonify({"estado": "ok", "mensaje": f"{clave} guardado."})

@app.route("/leer_memoria", methods=["POST"])
def leer_memoria():
    data = request.json
    clave = data.get("clave")

    with open(MEMORIA_PATH, "r", encoding="utf-8") as f:
        memoria = json.load(f)
    
    valor = memoria.get(clave)
    if valor is None:
        return jsonify({"estado": "error", "detalle": "Clave no encontrada."}), 404

    return jsonify({"estado": "ok", "valor": valor})

# -------- ARCHIVOS Y SCRIPTS --------
@app.route("/crear_funcion", methods=["POST"])
def crear_funcion():
    data = request.json
    nombre = data.get("nombre")
    contenido = data.get("contenido")

    ruta = f"{SCRIPTS_DIR}/{nombre}.py" if not nombre.endswith(".py") else f"{SCRIPTS_DIR}/{nombre}"

    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        return jsonify({"estado": "ok", "mensaje": f"Función guardada en {ruta}."})
    except Exception as e:
        return jsonify({"estado": "error", "detalle": str(e)}), 500

@app.route("/ejecutar_script", methods=["POST"])
def ejecutar_script():
    data = request.json
    nombre = data.get("nombre")

    ruta = f"{SCRIPTS_DIR}/{nombre}.py" if not nombre.endswith(".py") else f"{SCRIPTS_DIR}/{nombre}"

    if not os.path.exists(ruta):
        return jsonify({"estado": "error", "detalle": f"{ruta} no existe."}), 404

    try:
        resultado = subprocess.check_output(["python", ruta], stderr=subprocess.STDOUT, timeout=10)
        return jsonify({"estado": "ok", "resultado": resultado.decode("utf-8")})
    except subprocess.CalledProcessError as e:
        return jsonify({"estado": "error", "detalle": e.output.decode("utf-8")}), 500
    except Exception as e:
        return jsonify({"estado": "error", "detalle": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
