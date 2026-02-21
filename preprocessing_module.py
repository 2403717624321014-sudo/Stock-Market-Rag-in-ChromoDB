# file: preprocessing_module.py

import json
import re

def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove special characters and numbers from the text (keep alpha only for basic cleaning)
    text = re.sub(r'[^a-z\s]', '', text)
    # Remove extra whitespace
    text = " ".join(text.split())
    return text

def clean_prices(prices_list):
    clean_list = []
    for price in prices_list:
        # Remove commas and convert to float
        try:
            val = float(price.replace(',', ''))
            clean_list.append(val)
        except ValueError:
            continue
    return clean_list

def main():
    try:
        with open("nifty_corpus.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: nifty_corpus.json not found. Run data_collection_module.py first.")
        return

    processed_data = []

    for entry in data:
        processed_entry = {
            "source": entry.get("source"),
            "timestamp": entry.get("timestamp"),
            "clean_text": clean_text(entry.get("text", "")),
            "clean_prices": clean_prices(entry.get("prices_found", []))
        }
        processed_data.append(processed_entry)

    with open("processed_nifty_data.json", "w", encoding="utf-8") as f:
        json.dump(processed_data, f, indent=4)

    print("Preprocessing completed. Data saved to processed_nifty_data.json")

if __name__ == "__main__":
    main()