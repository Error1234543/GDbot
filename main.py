import os
import asyncio
import aiohttp
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from yt_dlp import YoutubeDL

API_ID = 20619533
API_HASH = "5893568858a096b7373c1970ba05e296"
BOT_TOKEN = "7764590689:AAFc4kG8_8hBRjye9MdsMndgwTfEPisSohE"
OWNER_ID = 7447651332
ALLOWED_GROUP = -1002432150473

app = Client("Solo-Leech-Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DOWNLOADS = "downloads"
if not os.path.exists(DOWNLOADS):
    os.makedirs(DOWNLOADS)


def human_readable_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


async def download_with_yt_dlp(url, path):
    ydl_opts = {
        'outtmpl': os.path.join(path, '%(title).80s.%(ext)s'),
        'format': 'best',
        'quiet': True,
        'noplaylist': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


@app.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if user_id != OWNER_ID and chat_id != ALLOWED_GROUP:
        await message.reply_text("❌ You are not allowed to use this bot.")
        return

    await message.reply_text("👋 Hello! Send me a video or PDF URL to start downloading.")


@app.on_message(filters.text & filters.private)
async def handle_url(client, message: Message):
    url = message.text.strip()
    user_id = message.from_user.id

    if user_id != OWNER_ID:
        await message.reply_text("⛔ Only the bot owner can use this.")
        return

    status = await message.reply_text("🔍 Fetching...")

    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        downloaded_file = await download_with_yt_dlp(url, DOWNLOADS)

        file_size = os.path.getsize(downloaded_file)
        await status.edit(f"✅ Download complete! Uploading `{os.path.basename(downloaded_file)}` ({human_readable_size(file_size)})")

        await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_DOCUMENT)
        await message.reply_document(downloaded_file, caption="📥 Here is your file!")

        os.remove(downloaded_file)

    except Exception as e:
        await status.edit(f"❌ Failed: {str(e)}")


app.run()