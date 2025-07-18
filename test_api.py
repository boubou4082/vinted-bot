import requests

url = "https://www.vinted.fr/api/v2/catalog/items"
params = {
    "search_text": "bubble bum",
    "price_to": 50,
    "currency": "EUR",
    "order": "newest_first",
    "per_page": 5
}
headers = {"User-Agent": "Mozilla/5.0"}

resp = requests.get(url, params=params, headers=headers)
print("Status code:", resp.status_code)
print("JSON keys:", resp.json().keys())
print("Nombre d'items:", len(resp.json().get("items", [])))
