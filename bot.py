from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
import handlers

app = Client("jacpotfilm_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

handlers.register_handlers(app)

print("🤖 Jacpotfilm Bot started — Full functional features ready.")
app.run()
