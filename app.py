import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
CORS(app)

ZUKI_API_KEY = os.getenv("ZUKIJOURNEY_API_KEY")
if not ZUKI_API_KEY:
    raise ValueError("ZUKIJOURNEY_API_KEY is not set in the environment. Please update your .env file.")

ZUKI_API_ENDPOINT = "https://api.zukijourney.com/v1/chat/completions"

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Lagoon AI backend is running!"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided."}), 400

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZUKI_API_KEY}"
    }
    
    payload = {
        "model": "gpt-4o",  
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    }
    
    try:
        response = requests.post(ZUKI_API_ENDPOINT, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            reply = result.get("choices", [{}])[0].get("message", {}).get("content", "No response generated.")
            return jsonify({"response": reply})
        else:
            return jsonify({
                "error": f"Failed with status code {response.status_code}: {response.text}"
            }), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
