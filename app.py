from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_API = "http://ollama:11434/api/chat"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    model = data.get("model", "llama2")

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": user_msg}],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API, json=payload)
        if response.status_code == 200:
            result = response.json()
            reply = result["message"]["content"]
            return jsonify({"reply": reply})
        else:
            return jsonify({"error": "Ollama error"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
