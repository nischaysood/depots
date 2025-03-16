import os
import telegram
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telegram.Bot(token=BOT_TOKEN)

async def send_test_message():
    try:
        await bot.send_message(chat_id=CHAT_ID, text="🚀 Test message from Arbitrage Bot!")
        print("✅ Telegram test message sent!")
    except Exception as e:
        print(f"⚠️ Error sending message: {e}")

# Run the async function properly
asyncio.run(send_test_message())