from flask import Flask, send_from_directory, jsonify, request
import requests

app = Flask(__name__)

# API Key de Riot Games
RIOT_API_KEY = "414fe9f9-9252-48a7-997a-f80313e96828"
REGION = "euw1"  # Cambia la región según corresponda (euw1, na1, etc.)

@app.route("/")
def home():
    return "Riot Games API Bot is running!"

@app.route("/riot.txt")
def serve_riot_file():
    try:
        # Sirve el archivo riot.txt desde el directorio actual
        return send_from_directory('.', 'riot.txt')
    except Exception as e:
        return jsonify({"error": "Error serving riot.txt", "details": str(e)}), 500

@app.route("/rank", methods=["GET"])
def get_rank():
    try:
        # Obtener el Act ID actual
        content_url = f"https://{REGION}.api.riotgames.com/val/content/v1/contents"
        headers = {"X-Riot-Token": RIOT_API_KEY}

        content_response = requests.get(content_url, headers=headers)
        if content_response.status_code != 200:
            return jsonify({"error": "Failed to fetch Act ID", "details": content_response.json()}), content_response.status_code

        content_data = content_response.json()
        act_id = None
        for act in content_data["acts"]:
            if act["isActive"]:
                act_id = act["id"]
                break

        if not act_id:
            return jsonify({"error": "No active Act ID found"}), 404

        # Consultar el leaderboard usando el Act ID
        leaderboard_url = f"https://{REGION}.api.riotgames.com/val/ranked/v1/leaderboards/by-act/{act_id}"
        leaderboard_response = requests.get(leaderboard_url, headers=headers)
        if leaderboard_response.status_code != 200:
            return jsonify({"error": "Failed to fetch leaderboard", "details": leaderboard_response.json()}), leaderboard_response.status_code

        leaderboard_data = leaderboard_response.json()
        return jsonify(leaderboard_data)

    except Exception as e:
        return jsonify({"error": "Unexpected server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
