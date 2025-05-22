
from flask import Flask, request, jsonify
import os
import time

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ AEGON está en línea"

@app.route("/crear_archivo", methods=["POST"])
def crear_archivo():
    data = request.json
    nombre = data.get("nombre")
    contenido = data.get("contenido")
    try:
        with open(nombre, "w", encoding="utf-8") as f:
            f.write(contenido)
        return jsonify({"estado": "ok", "mensaje": f"Archivo {nombre} creado correctamente."}), 200
    except Exception as e:
        return jsonify({"estado": "error", "detalle": str(e)}), 500

@app.route("/leer_archivo", methods=["POST"])
def leer_archivo():
    data = request.json
    nombre = data.get("nombre")
    try:
        with open(nombre, "r", encoding="utf-8") as f:
            contenido = f.read()
        return jsonify({"estado": "ok", "contenido": contenido}), 200
    except Exception as e:
        return jsonify({"estado": "error", "detalle": str(e)}), 500

@app.route("/crear_funcion", methods=["POST"])
def crear_funcion():
    data = request.json
    nombre = data.get("nombre")
    contenido = data.get("contenido")
    try:
        ruta = f"{nombre}.py" if not nombre.endswith(".py") else nombre
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        return jsonify({"estado": "ok", "mensaje": f"Función {ruta} creada."}), 200
    except Exception as e:
        return jsonify({"estado": "error", "detalle": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
