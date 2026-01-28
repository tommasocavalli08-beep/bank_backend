from flask import Flask, request, jsonify
from flask_cors import CORS
from ai import call_ai, generate_mail
import os
import random

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("OLLAMA_API_KEY")

CHAT_SYSTEM = {
    "role": "system",
    "content": "Sei un assistente interno di banca. Tono freddo e professionale."
}

chat_history = [CHAT_SYSTEM]

# STATO GIOCO
bank_fund = 1_000_000

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

    # assegna tipo e importo
    mail_type = random.choice(["loan", "fraud", "audit", "generic"])
    amount = random.randint(5_000, 150_000) if mail_type == "loan" else 0

    return jsonify({
        "title": mail["title"],
        "body": mail["body"],
        "type": mail_type,
        "amount": amount
    })


@app.route("/decision", methods=["POST"])
def decision():
    global bank_fund
    data = request.json

    if data["type"] == "loan" and data["action"] == "APPROVATA":
        bank_fund -= data["amount"]

    if data["type"] == "fraud" and data["action"] == "SEGNALATA":
        bank_fund += 20_000

    return jsonify({"bank_fund": bank_fund})


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"bank_fund": bank_fund})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
