from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Server is running!"

@app.route("/rank")
def rank():
    return {"rank": "Test Rank"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)