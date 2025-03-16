import os
import ccxt
import json
from dotenv import load_dotenv

print("🚀 Starting fetch_prices.py...")

# Load API keys
load_dotenv()

# Debug: Check if API keys are loaded
print("🔑 Binance API Key:", os.getenv("BINANCE_API_KEY"))
print("🔑 KuCoin API Key:", os.getenv("KUCOIN_API_KEY"))

# Initialize Binance with API keys
binance = ccxt.binance({
    'apiKey': os.getenv("BINANCE_API_KEY"),
    'secret': os.getenv("BINANCE_SECRET_KEY"),
    'options': {'defaultType': 'spot'}
})

# Initialize KuCoin with API keys
kucoin = ccxt.kucoin({
    'apiKey': os.getenv("KUCOIN_API_KEY"),
    'secret': os.getenv("KUCOIN_SECRET_KEY"),
    'password': os.getenv("KUCOIN_PASSPHRASE"),
})

print("✅ Exchanges initialized successfully!")

def get_price(symbol):
    """Fetch latest prices from Binance and KuCoin"""
    print(f"🔍 Fetching prices for {symbol}...")
    try:
        binance_price = binance.fetch_ticker(symbol)['last']
        kucoin_price = kucoin.fetch_ticker(symbol)['last']
        print(f"📊 Prices - Binance: {binance_price}, KuCoin: {kucoin_price}")

        # Save prices to a JSON file
        prices = {"binance": binance_price, "kucoin": kucoin_price}
        with open("prices.json", "w") as file:
            json.dump(prices, file, indent=4)

        return prices
    except Exception as e:
        print(f"❌ Error fetching prices: {e}")
        return None

# Run test
import time

print("🚀 Starting automated price fetch...")

while True:
    get_price("BTC/USDT")
    print("✅ Prices saved! Checking arbitrage...\n")
    time.sleep(10)  # Wait 10 seconds before the next check