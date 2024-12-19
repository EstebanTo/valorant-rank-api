from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_KEY = "49cd803b-0712-4357-8be0-2bd757c79719"
PLAYER_PROFILE = "3cm 5secs#fin"

@app.route('/rank', methods=['GET'])
def get_rank():
    headers = {"TRN-Api-Key": API_KEY}
    url = f"https://api.tracker.gg/api/v2/valorant/standard/profile/riot/{PLAYER_PROFILE.replace('#', '%23')}"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            rank = data['data']['segments'][0]['stats']['rank']['metadata']['tierName']
            return jsonify({"rank": rank})
        except KeyError:
            return jsonify({"error": "Rank not found"}), 404
    else:
        return jsonify({"error": "API request failed"}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
