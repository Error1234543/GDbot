from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 20619533
API_HASH = "5893568858a096b7373c1970ba05e296"
BOT_TOKEN = "7764590689:AAFc4kG8_8hBRjye9MdsMndgwTfEPisSohE"
OWNER_ID = 7447651332
ALLOWED_GROUP = -1002432150473

app = Client("Solo-Leech-Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if user_id != OWNER_ID and chat_id != ALLOWED_GROUP:
        await message.reply_text("🚫 Access Denied!\n\nYou are not authorized to use this bot.")
        return

    await message.reply_text("✅ Bot is up and running!\n\nSend a command to begin.")

app.run()