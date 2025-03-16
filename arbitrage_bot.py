import ccxt

# Define the exchanges we want to compare
exchange1 = ccxt.binance()
exchange2 = ccxt.coinbase()

# Fetch prices
symbol = "BTC/USDT"
binance_price = exchange1.fetch_ticker(symbol)["last"]
coinbase_price = exchange2.fetch_ticker(symbol)["last"]

print(f"Binance Price: {binance_price}")
print(f"Coinbase Price: {coinbase_price}")

# Check for arbitrage opportunity
if binance_price < coinbase_price:
    print(f"Arbitrage Opportunity! Buy on Binance at {binance_price}, sell on Coinbase at {coinbase_price}")
elif binance_price > coinbase_price:
    print(f"Arbitrage Opportunity! Buy on Coinbase at {coinbase_price}, sell on Binance at {binance_price}")
else:
    print("No arbitrage opportunity found.")