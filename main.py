from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/", methods=["POST"])
def alice():
    r = requests.get(
        f"https://generativelanguage.googleapis.com/v1/models?key={GEMINI_API_KEY}"
    )
    models = r.json()
    names = [m.get("name","") for m in models.get("models",[])][:10]
    answer = ", ".join(names) if names else str(r.json())[:500]
    return jsonify({"response": {"text": answer, "end_session": False}, "version": "1.0"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
