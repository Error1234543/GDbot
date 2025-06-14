import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
ALLOWED_GROUP = int(os.getenv("ALLOWED_GROUP"))

app = Client("Solo-Leech-Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    if message.from_user.id != OWNER_ID:
        await message.reply_text("🚫 Access Denied!")
        return
    await message.reply_text("✅ Bot is up and running!")

app.run()