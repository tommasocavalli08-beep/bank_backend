import requests

OLLAMA_URL = "https://ollama.com/api/chat"
MODEL = "cogito-2.1:671b"

def call_ai(api_key, messages, temperature=0.7):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "stream": False
    }

    r = requests.post(OLLAMA_URL, json=payload, headers=headers)
    r.raise_for_status()
    data = r.json()

    return data["message"]["content"]


def generate_mail(api_key):
    messages = [
        {
            "role": "system",
            "content": (
                "Genera una mail interna per un operatore di banca. "
                "Tema realistico (mutuo, audit, segnalazione sospetta, cliente). "
                "Scrivi titolo e corpo separati da ||."
                "Scrivi in formato JSON: {\"title\": \"...\", \"body\": \"...\"}"
            )
        }
    ]

    text = call_ai(api_key, messages, temperature=0.9)

    # ====== QUI il fix ======
    if "||" in text:
        title, body = text.split("||", 1)
    else:
        # se l'AI non mette ||, crea un titolo automatico
        title = "Mail interna — " + text[:30].strip()
        body = text

    return {
        "title": title.strip(),
        "body": body.strip()
    }
