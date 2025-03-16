import os
import json
import time
import telegram
import asyncio
import ccxt
from dotenv import load_dotenv

# Load API keys
load_dotenv()

# Telegram Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telegram.Bot(token=BOT_TOKEN)

# Binance & KuCoin API keys
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY")
KUCOIN_SECRET_KEY = os.getenv("KUCOIN_SECRET_KEY")
KUCOIN_PASSPHRASE = os.getenv("KUCOIN_PASSPHRASE")

# Initialize exchanges
binance = ccxt.binance({
    'apiKey': BINANCE_API_KEY,
    'secret': BINANCE_SECRET_KEY,
    'options': {'defaultType': 'spot'}
})

kucoin = ccxt.kucoin({
    'apiKey': KUCOIN_API_KEY,
    'secret': KUCOIN_SECRET_KEY,
    'password': KUCOIN_PASSPHRASE,
})

async def send_alert(message):
    """Send alert to Telegram"""
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
        print("📩 Telegram alert sent!")
    except Exception as e:
        print(f"⚠️ Error sending Telegram message: {e}")

def execute_trade(exchange, symbol, side, amount):
    """Execute a trade on the given exchange"""
    try:
        order = exchange.create_market_order(symbol, side, amount)
        print(f"✅ Trade executed: {side} {amount} {symbol} on {exchange.id}")
        return order
    except Exception as e:
        print(f"❌ Trade execution failed: {e}")
        return None

def find_arbitrage():
    """Check for arbitrage opportunities and execute trades"""
    try:
        with open("prices.json", "r") as file:
            prices = json.load(file)

        binance_price = prices["binance"]
        kucoin_price = prices["kucoin"]
        symbol = "BTC/USDT"
        trade_amount = 0.001  # Adjust trade amount as needed

        if binance_price < kucoin_price:
            profit = kucoin_price - binance_price
            alert_msg = f"💰 Arbitrage Opportunity! Buy on Binance at ${binance_price}, sell on KuCoin at ${kucoin_price}. Profit: ${profit:.2f}"
            print(alert_msg)

            # Execute trades
            execute_trade(binance, symbol, "buy", trade_amount)
            execute_trade(kucoin, symbol, "sell", trade_amount)

            # Send alert
            asyncio.run(send_alert(alert_msg))

        elif kucoin_price < binance_price:
            profit = binance_price - kucoin_price
            alert_msg = f"💰 Arbitrage Opportunity! Buy on KuCoin at ${kucoin_price}, sell on Binance at ${binance_price}. Profit: ${profit:.2f}"
            print(alert_msg)

            # Execute trades
            execute_trade(kucoin, symbol, "buy", trade_amount)
            execute_trade(binance, symbol, "sell", trade_amount)

            # Send alert
            asyncio.run(send_alert(alert_msg))

        else:
            print("❌ No arbitrage opportunity at the moment.")

    except Exception as e:
        print(f"⚠️ Error in arbitrage calculation: {e}")

# Run arbitrage check in a loop
while True:
    find_arbitrage()
    print("🔄 Waiting for next check...\n")
    time.sleep(10)  # Run every 10 seconds