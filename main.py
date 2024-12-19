from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Configuración de la API
API_KEY = "f7f87a6a-9d98-4f1a-8ec9-ff467386a9ad"  # Nueva clave API
PLAYER_PROFILE = "3cm 5secs#fin"  # Cambia esto por el ID del jugador si es necesario

@app.route("/")
def home():
    return "Server is running!"

@app.route("/rank", methods=["GET"])
def get_rank():
    headers = {
        "TRN-Api-Key": API_KEY,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = f"https://api.tracker.gg/api/v2/valorant/standard/profile/riot/{PLAYER_PROFILE.replace('#', '%23')}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            rank = data['data']['segments'][0]['stats']['rank']['metadata']['tierName']
            return rank  # Devuelve solo el rango como texto plano
        else:
            return jsonify({
                "error": "API request failed",
                "status_code": response.status_code,
                "response_text": response.text
            }), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
