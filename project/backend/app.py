from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__, static_folder='.')

CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
print(OPENROUTER_API_KEY)

@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": """
                You are Aurora Elite AI,
                a futuristic luxury travel assistant.

                Speak professionally,
                elegantly,
                and help users discover
                premium travel experiences.
                """
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Aurora Elite AI",
        "Content-Type": "application/json"
    },
    json=data
)

    result = response.json()
    print(result)

    try:
        ai_response = result["choices"][0]["message"]["content"]
    except:
        ai_response = "Aurora Elite AI is temporarily unavailable."

    return jsonify({
        "response": ai_response
    })

if __name__ == "__main__":
    app.run(debug=True)