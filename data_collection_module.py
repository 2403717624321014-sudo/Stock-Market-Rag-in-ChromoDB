# file: data_collection_module.py

import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime

# -------------------------
# CONFIG
# -------------------------
URLS = [
    "https://www.moneycontrol.com/indian-indices/nifty-50-9.html",
    "https://economictimes.indiatimes.com/markets/stocks"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (NIFTY academic project)"
}

# -------------------------
# FETCH PAGE
# -------------------------
def fetch_page(url):
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return response.text

# -------------------------
# EXTRACT TEXT
# -------------------------
def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    paragraphs = []
    for p in soup.find_all("p"):
        text = p.get_text(" ", strip=True)
        if len(text) > 40:
            paragraphs.append(text)

    return "\n".join(paragraphs)

# -------------------------
# EXTRACT PRICE (Basic Regex)
# -------------------------
def extract_prices(text):
    # finds numbers like 22,150.35
    prices = re.findall(r"\d{1,3}(?:,\d{3})*(?:\.\d+)?", text)
    return prices[:10]  # return first few matches

# -------------------------
# MAIN
# -------------------------
def main():
    corpus_data = []

    for url in URLS:
        print("Fetching:", url)
        html = fetch_page(url)
        clean_text = extract_text(html)
        prices = extract_prices(clean_text)

        entry = {
            "source": url,
            "timestamp": str(datetime.now()),
            "text": clean_text[:2000],  # limit size
            "prices_found": prices
        }

        corpus_data.append(entry)

    # Save corpus for next module
    with open("nifty_corpus.json", "w", encoding="utf-8") as f:
        json.dump(corpus_data, f, indent=4)

    print("\nData collection completed.")
    print("Saved to nifty_corpus.json")

if __name__ == "__main__":
    main()