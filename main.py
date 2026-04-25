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
        return jsonify({"response": {"text": "Привет! Задай вопрос.", "end_session": False}, "version": "1.0"})
    try:
        r = requests.post(
            f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}",
            json={"contents": [{"parts": [{"text": user_text}]}]}
        )
        resp = r.json()
        if "candidates" in resp:
            answer = resp["candidates"][0]["content"]["parts"][0]["text"][:1000]
        else:
            answer = str(resp)[:1000]
    except Exception as e:
        answer = str(e)[:500]
    return jsonify({"response": {"text": answer, "end_session": False}, "version": "1.0"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
