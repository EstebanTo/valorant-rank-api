from flask import Flask, jsonify, request, redirect
import requests

app = Flask(__name__)

# API Key de Riot Games
RIOT_API_KEY = "414fe9f9-9252-48a7-997a-f80313e96828"

# Región del servidor (ajusta según corresponda)
REGION = "na1"  # Usa "euw1" para Europa, "na1" para Norteamérica, etc.

@app.route('/riot.txt')
def serve_riot_file():
    return send_from_directory('.', 'riot.txt')
    
@app.route("/")
def home():
    return "Riot Games API Bot is running!"

@app.route("/rank", methods=["GET"])
def get_rank():
    try:
        # Obtener el Act ID actual (necesario para consultar clasificaciones)
        content_url = f"https://{REGION}.api.riotgames.com/val/content/v1/contents"
        headers = {"X-Riot-Token": RIOT_API_KEY}

        content_response = requests.get(content_url, headers=headers)
        if content_response.status_code != 200:
            return jsonify({"error": "Failed to fetch Act ID", "details": content_response.json()}), content_response.status_code

        # Extraer el Act ID activo
        content_data = content_response.json()
        act_id = None
        for act in content_data["acts"]:
            if act["isActive"]:
                act_id = act["id"]
                break

        if not act_id:
            return jsonify({"error": "No active Act ID found"}), 404

        # Consultar clasificaciones por Act ID
        leaderboard_url = f"https://{REGION}.api.riotgames.com/val/ranked/v1/leaderboards/by-act/{act_id}"
        leaderboard_response = requests.get(leaderboard_url, headers=headers)
        if leaderboard_response.status_code != 200:
            return jsonify({"error": "Failed to fetch leaderboard", "details": leaderboard_response.json()}), leaderboard_response.status_code

        leaderboard_data = leaderboard_response.json()
        return jsonify(leaderboard_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
