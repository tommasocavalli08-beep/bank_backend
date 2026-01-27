from flask import Flask, request, jsonify
from flask_cors import CORS
from ai import call_ai, generate_mail
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("OLLAMA_API_KEY")

CHAT_SYSTEM = {
    "role": "system",
    "content": (
        "Sei un assistente interno di una banca. "
        "Tono professionale, freddo, burocratico."
    )
}

chat_history = [CHAT_SYSTEM]

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]

    chat_history.append({"role": "user", "content": user_msg})
    reply = call_ai(API_KEY, chat_history)
    chat_history.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})


@app.route("/new-mail", methods=["GET"])
def new_mail():
    mail = generate_mail(API_KEY)
    return jsonify(mail)


if __name__ == "__main__":
    app.run()
