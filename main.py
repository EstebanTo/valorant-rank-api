from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Obtén la clave de la API desde las variables de entorno
API_KEY = os.getenv("TRN_API_KEY", "your_default_api_key")
PLAYER_PROFILE = "3cm 5secs#fin"

@app.route("/")
def home():
    return "Server is running!"

@app.route("/rank", methods=["GET"])
def get_rank():
    headers = {"TRN-Api-Key": API_KEY}
    url = f"https://api.tracker.gg/api/v2/valorant/standard/profile/riot/{PLAYER_PROFILE.replace('#', '%23')}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            rank = data['data']['segments'][0]['stats']['rank']['metadata']['tierName']
            return jsonify({"rank": rank})
        else:
            return jsonify({"error": f"API request failed with status {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
