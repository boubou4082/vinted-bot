import requests
from bs4 import BeautifulSoup

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1395783915909943428/DeM-PnAVXSLjofWEPh4Nx37HqhatVpaVhTPJ6I1T6Hfiy4VBZE906SXAk_6AiGDf-gSv"

KEYWORDS = [
    "bubble bum",
    "bubblebum",
    "réhausseur gonflable",
    "siège auto gonflable",
    "mifold"
]

def search_vinted_html(query):
    url = f"https://www.vinted.fr/catalog?search_text={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    items = []
    for article in soup.find_all("article", class_="feed-grid__item"):
        title_tag = article.find("h3", class_="feed-item__title")
        price_tag = article.find("div", class_="feed-item__price")
        link_tag = article.find("a", class_="feed-item__link")

        if title_tag and price_tag and link_tag:
            title = title_tag.text.strip()
            price_text = price_tag.text.strip().replace("€", "").replace(",", ".").strip()
            try:
                price = float(price_text)
            except:
                price = 0
            url = "https://www.vinted.fr" + link_tag.get("href")
            items.append({"title": title, "price": price, "url": url})
    return items

def notify_discord(item):
    message = f"🆕 {item['title']} - {item['price']}€\n➡️ {item['url']}"
    data = {"content": message}
    requests.post(DISCORD_WEBHOOK, json=data)

def run():
    seen_titles = set()
    for keyword in KEYWORDS:
        print(f"Recherche : {keyword}")
        items = search_vinted_html(keyword)
        for item in items:
            if item["title"] not in seen_titles and item["price"] <= 50:
                seen_titles.add(item["title"])
                print(f"Trouvé : {item['title']} - {item['price']}€")
                notify_discord(item)

if __name__ == "__main__":
    run()
