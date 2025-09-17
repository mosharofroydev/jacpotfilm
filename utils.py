from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime, asyncio
from config import FORWARD_PROTECT, ADVANCED_FORWARD, BRANDING_TEXT, VIDEO_EXPIRY_DAYS

def regex_match(query, items):
    return [item for item in items if query.lower() in item.lower()]

def smart_suggest(query, items):
    return items  # AI spell check placeholder

async def auto_delete(message, delay=300):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except:
        pass

def set_video_expiry(file_id, days=VIDEO_EXPIRY_DAYS):
    return datetime.datetime.now() + datetime.timedelta(days=days)

def add_branding(thumbnail_path):
    return f"{BRANDING_TEXT} | {thumbnail_path}"

def protect_forward():
    return FORWARD_PROTECT

def advanced_forward():
    return ADVANCED_FORWARD

def build_buttons(items, prefix, max_buttons=8):
    buttons, row = [], []
    for i, item in enumerate(items, 1):
        row.append(InlineKeyboardButton(str(item), callback_data=f"{prefix}_{item}"))
        if i % 2 == 0 or i == len(items):
            buttons.append(row)
            row = []
    return InlineKeyboardMarkup(buttons)
