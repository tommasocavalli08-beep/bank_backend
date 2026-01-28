import requests
import random

OLLAMA_URL = "https://ollama.com/api/chat"
MODEL = "cogito-2.1:671b"

NOMI = ["Marco", "Luca", "Giulia", "Anna", "Paolo", "Sara", "Davide"]
COGNOMI = ["Rossi", "Bianchi", "Verdi", "Conti", "Moretti", "Gallo", "Ferrari"]

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
    return r.json()["message"]["content"]


def generate_mail(api_key):
    nome = random.choice(NOMI)
    cognome = random.choice(COGNOMI)

    system_prompt = f"""
Sei un sistema interno di una banca.
Genera UNA mail realistica.
NON usare JSON.
NON usare parentesi.
NON scrivere spiegazioni.

Formato OBBLIGATORIO (una sola volta):
TITOLO:
<titolo>

CORPO:
<testo>

Usa nomi realistici (es: {nome} {cognome}).
Temi possibili:
- mutuo
- prestito
- segnalazione sospetta
- audit
- investimento
"""

    text = call_ai(api_key, [
        {"role": "system", "content": system_prompt}
    ], temperature=0.9)

    if "CORPO:" not in text:
        return {
            "title": "Comunicazione interna",
            "body": text.strip()
        }

    title = text.split("TITOLO:")[1].split("CORPO:")[0].strip()
    body = text.split("CORPO:")[1].strip()

    return {
        "title": title,
        "body": body
    }
