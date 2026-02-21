# file: indicators_module.py

import json

def calculate_sma(prices, window=3):
    """Calculates Simple Moving Average."""
    if len(prices) < window:
        return None
    sma = sum(prices[:window]) / window
    return round(sma, 2)

def calculate_rsi(prices, window=14):
    """Placeholder for RSI calculation logic."""
    # RSI requires more data points than we currently have in the sample
    # Typically: RSI = 100 - (100 / (1 + RS))
    return "Insufficient data for RSI"

def main():
    try:
        with open("processed_nifty_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: processed_nifty_data.json not found. Run preprocessing_module.py first.")
        return

    print("--- Financial Indicators Analysis ---")
    for entry in data:
        prices = entry.get("clean_prices", [])
        source = entry.get("source")
        
        print(f"\nSource: {source}")
        if not prices:
            print("No price data found in this source.")
            continue
            
        sma_val = calculate_sma(prices)
        rsi_val = calculate_rsi(prices)
        
        print(f"Prices detected: {prices}")
        print(f"SMA (window=3): {sma_val}")
        print(f"RSI Status: {rsi_val}")

if __name__ == "__main__":
    main()