from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/", methods=["POST"])
def alice():
    data = request.json
    user_text = data.get("request", {}).get("original_utterance", "")
    
    if not user_text:
        return jsonify({"response": {"text": "Привет! Задай мне любой вопрос.", "end_session": False}, "version": "1.0"})
    
    try:
        r = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}",
            json={"contents": [{"parts": [{"text": user_text}]}]}
        )
        answer = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        answer = answer[:1000]
    except Exception as e:
    answer = f"Ошибка: {str(e)}"
    
    return jsonify({"response": {"text": answer, "end_session": False}, "version": "1.0"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
