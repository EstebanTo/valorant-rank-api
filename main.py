from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Configuración
RIOT_API_KEY = "RGAPI-01c33de7-ce03-4407-b403-da2ec374ee89"  # Sustituye por tu clave
REGION = "euw1"  # Cambia según la región del jugador
PLAYER_NAME = "3cm 5secs"  # Nombre del jugador
PLAYER_TAG = "fin"  # Tag del jugador

@app.route("/")
def home():
    return "Riot Games API Bot is running!"

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

        # Consultar el leaderboard para el Act ID
        leaderboard_url = f"https://{REGION}.api.riotgames.com/val/ranked/v1/leaderboards/by-act/{act_id}?size=200&startIndex=0"
        leaderboard_response = requests.get(leaderboard_url, headers=headers)

        if leaderboard_response.status_code != 200:
            return jsonify({"error": "Failed to fetch leaderboard", "details": leaderboard_response.json()}), leaderboard_response.status_code

        leaderboard_data = leaderboard_response.json()
        for player in leaderboard_data["players"]:
            if player["gameName"] == PLAYER_NAME and player["tagLine"] == PLAYER_TAG:
                return jsonify({
                    "gameName": player["gameName"],
                    "tagLine": player["tagLine"],
                    "rankedRating": player["rankedRating"],
                    "leaderboardRank": player["leaderboardRank"],
                    "numberOfWins": player["numberOfWins"]
                })

        return jsonify({"error": "Player not found in leaderboard"}), 404

    except Exception as e:
        return jsonify({"error": "Unexpected server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
