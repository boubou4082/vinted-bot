import requests
import time

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1395783915909943428/DeM-PnAVXSLjofWEPh4Nx37HqhatVpaVhTPJ6I1T6Hfiy4VBZE906SXAk_6AiGDf-gSv"

SEARCH_URL = "https://www.vinted.fr/api/v2/catalog/items"

# Mots-clés à surveiller
KEYWORDS = [
    "bubble bum",
    "bubblebum",
    "réhausseur gonflable",
    "siège auto gonflable",
    "mifold"
]

def search_items(query):
    params = {
        "search_text": query,
        "price_to": 50,
        "currency": "EUR",
        "order": "newest_first",
        "per_page": 10
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(SEARCH_URL, params=params, headers=headers)
    return response.json().get("items", [])

def notify_discord(item):
    message = f"🆕 {item['title']} - {item['price']}€\n➡️ https://www.vinted.fr/items/{item['id']}"
    data = {"content": message}
    requests.post(DISCORD_WEBHOOK, json=data)

def run():
    seen_ids = set()
    for keyword in KEYWORDS:
        print(f"Recherche : {keyword}")
        items = search_items(keyword)
        for item in items:
            if item["id"] not in seen_ids:
                seen_ids.add(item["id"])
                print(f"Trouvé : {item['title']} - {item['price']}€")
                print(f"https://www.vinted.fr/items/{item['id']}")
                notify_discord(item)

if __name__ == "__main__":
    run()
