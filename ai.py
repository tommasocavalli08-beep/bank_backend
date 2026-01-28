import requests

OLLAMA_URL = "https://ollama.com/api/chat"
MODEL = "cogito-2.1:671b"

def call_ai(api_key, messages, temperature=0.45):
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
            messages = [
    {
        "role": "system",
        "content": (
            "Sei un generatore di email per un videogioco gestionale bancario.\n"
            "Devi generare UNA mail realistica ogni volta.\n\n"

            "REGOLE OBBLIGATORIE:\n"
            "- NON usare JSON\n"
            "- NON usare virgolette\n"
            "- NON scrivere spiegazioni\n"
            "- NON scrivere parentesi quadre o segnaposto\n"
            "- NON ripetere la parola titolo o body\n\n"

            "FORMATO OBBLIGATORIO (UNA SOLA VOLTA):\n"
            "Titolo della mail || Corpo della mail\n\n"

            "CONTENUTO:\n"
            "- Inventa sempre nome e cognome realistici italiani\n"
            "- Inventa casi bancari diversi (prestiti, mutui, frodi, audit, reclami, investimenti)\n"
            "- Tono professionale interno\n"
            "- Lunghezza media\n\n"

            "ESEMPIO CORRETTO:\n"
            "Richiesta chiarimenti su finanziamento || Gentile collega, ti segnalo che..."
        )
    }
]

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

