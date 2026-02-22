# file: statistical_analysis_module.py

import re
import statistics

def extract_prices(text):
    numbers = re.findall(r"\d{1,3}(?:,\d{3})*(?:\.\d+)?", text)
    return [float(n.replace(',', '')) for n in numbers]

def analyze_documents(documents):

    all_prices = []

    for doc in documents:
        all_prices.extend(extract_prices(doc))

    if not all_prices:
        return {"Status": "No numeric stock data found."}

    mean_price = round(statistics.mean(all_prices), 2)
    max_price = round(max(all_prices), 2)
    min_price = round(min(all_prices), 2)

    std_dev = round(statistics.stdev(all_prices), 2) if len(all_prices) > 1 else 0
    volatility = std_dev

    if volatility < 20:
        risk = "[LOW RISK]"
    elif volatility < 50:
        risk = "[MEDIUM RISK]"
    else:
        risk = "[HIGH RISK]"

    trend = "[BULLISH TREND]" if all_prices[-1] > all_prices[0] else "[BEARISH TREND]"
    signal = "[BUY RECOMMENDED]" if "BULLISH" in trend else "[SELL RECOMMENDED]"

    return {
        "Mean Price": mean_price,
        "Max Price": max_price,
        "Min Price": min_price,
        "Volatility": volatility,
        "Risk Level": risk,
        "Trend": trend,
        "Trading Signal": signal
    }