from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import *
import utils
from config import ADMINS, TUTORIAL_MODE, ENABLE_ADS, FORWARD_PROTECT
import asyncio
import datetime

def register_handlers(app):

    @app.on_message(filters.command("start"))
    async def start(client, message):
        save_user(message.from_user.id, message.from_user.username)
        await message.reply_text("👋 Welcome! Search series name to start.")

    @app.on_message(filters.text & ~filters.command(["start"]))
    async def search_series(client, message):
        series_name = message.text.strip()
        save_user(message.from_user.id, message.from_user.username)
        seasons = get_seasons(series_name)
        if not seasons:
            await message.reply_text("❌ No series found.")
            return
        buttons = utils.build_buttons(seasons, f"season_{series_name}")
        msg = await message.reply_text(f"📺 Seasons for {series_name}:", reply_markup=buttons)
        asyncio.create_task(utils.auto_delete(msg, delay=300))

    @app.on_callback_query()
    async def callback(client, query):
        data = query.data

        if data.startswith("season_"):
            _, series_name, season = data.split("_", 2)
            episodes = get_episodes(series_name, season)
            if not episodes:
                await query.message.edit_text("❌ No episodes found.")
                return
            buttons = [[InlineKeyboardButton(ep["episode"], callback_data=f"ep_{series_name}_{season}_{ep['episode']}")] for ep in episodes]
            await query.message.edit_text(f"🎬 Episodes in Season {season}:", reply_markup=InlineKeyboardMarkup(buttons))

        elif data.startswith("ep_"):
            _, series_name, season, episode_name = data.split("_", 3)
            video_data = get_video(series_name, season, episode_name)
            if not video_data:
                await query.message.edit_text("❌ Video not available yet.")
                return
            verify_link = f"https://verify.example.com/{series_name}_{season}_{episode_name}_{query.from_user.id}"
            save_verify_link(query.from_user.id, verify_link)
            if ENABLE_ADS:
                track_ad_click(verify_link, query.from_user.id)

            buttons = [
                [InlineKeyboardButton("✅ Verify Link", url=verify_link)],
                [InlineKeyboardButton("📋 Copy Link", callback_data=f"copy_{verify_link}")]
            ]
            if TUTORIAL_MODE:
                buttons.append([InlineKeyboardButton("📘 Tutorial", url="https://tutorial.example.com")])

            await query.message.edit_text(
                f"▶️ {series_name} S{season}E{episode_name}\nPlease verify below.",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

            # Send video
            await send_video(query.from_user.id, video_data["file_id"], f"{series_name} S{season}E{episode_name}")

        elif data.startswith("copy_"):
            _, link = data.split("_", 1)
            await query.answer(f"Copied link: {link}", show_alert=True)

    async def send_video(user_id, file_id, caption=""):
        from bot import app as client
        thumbnail = utils.add_branding("default_thumbnail.jpg")
        msg = await client.send_video(
            chat_id=user_id,
            video=file_id,
            caption=caption,
            thumb=thumbnail,
            protect=FORWARD_PROTECT
        )
        log_action("video_sent", user_id, {"file_id": file_id})
        expiry_time = utils.set_video_expiry(file_id)
        delay = (expiry_time - datetime.datetime.now()).total_seconds()
        asyncio.create_task(utils.auto_delete(msg, delay=delay))
