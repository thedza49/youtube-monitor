import os
import logging
import asyncio
from datetime import time
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, Application
from delivery import DeliveryManager
from poller import YouTubePoller
from summarizer import VideoSummarizer

# Setup
load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

delivery = DeliveryManager()
AUTHORIZED_CHAT_ID = os.getenv("TELEGRAM_CHANNEL_ID")
THREAD_ID = int(os.getenv("TELEGRAM_THREAD_ID", 0)) or None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "channels.yaml")
SEEN_VIDEOS_PATH = os.path.join(BASE_DIR, "data", "seen_videos.json")
SUMMARIES_DIR = os.path.join(BASE_DIR, "data", "summaries")


def is_authorized(update: Update) -> bool:
    return str(update.effective_chat.id) == AUTHORIZED_CHAT_ID


async def run_pipeline(bot):
    """Core logic: poll, summarize, send. Used by both /fetch and the scheduler."""
    logger.info("Pipeline started")
    os.makedirs(SUMMARIES_DIR, exist_ok=True)

    try:
        poller = YouTubePoller(CONFIG_PATH, SEEN_VIDEOS_PATH)
        new_videos = poller.poll()
    except Exception as e:
        logger.error(f"Poller error: {e}")
        await bot.send_message(chat_id=AUTHORIZED_CHAT_ID, message_thread_id=THREAD_ID, text=f"Error scanning channels: {e}")
        return

    if not new_videos:
        logger.info("No new videos found")
        await bot.send_message(chat_id=AUTHORIZED_CHAT_ID, message_thread_id=THREAD_ID, text="No new videos found.")
        return

    await bot.send_message(chat_id=AUTHORIZED_CHAT_ID, message_thread_id=THREAD_ID, text=f"Found {len(new_videos)} new video(s). Summarizing...")

    # Mark as seen before processing to avoid duplicates on reruns
    seen = poller.seen_videos + [v['id'] for v in new_videos]
    poller.save_seen_videos(seen)

    summarizer = VideoSummarizer()

    for video in new_videos:
        video_id = video['id']
        title = video['title']
        link = video['link']
        channel_name = video.get('channel_name', 'Unknown Channel')
        summary_focus = video.get('summary_focus', 'general interest')

        logger.info(f"Summarizing: {title}")

        prompt_text = (
            f"Channel: {channel_name}\n"
            f"Title: {title}\n"
            f"URL: {link}\n"
            f"Summary focus: {summary_focus}"
        )

        try:
            summary_md = summarizer.summarize(video_id, title, channel_name, link, summary_focus)
        except Exception as e:
            logger.error(f"Summarizer error for {video_id}: {e}")
            summary_md = f"Summarization failed: {e}"

        await bot.send_message(
                chat_id=AUTHORIZED_CHAT_ID,
                text=f"*{title}*\n{link}\n\n{summary_md[:3000]}",
                parse_mode="Markdown"
            )

    await bot.send_message(chat_id=AUTHORIZED_CHAT_ID, message_thread_id=THREAD_ID, text=f"Done! Processed {len(new_videos)} video(s).")


async def scheduled_fetch(context):
    """Called automatically by the scheduler every day at 7pm PST."""
    logger.info("Scheduled fetch triggered")
    await run_pipeline(context.bot)


async def fetch_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manual /fetch command."""
    if not is_authorized(update):
        return
    await update.message.reply_text("Scanning for new videos...")
    await run_pipeline(context.bot)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    help_msg = (
        "@YTSum49bot | YouTube Summarizer\n\n"
        "Available Commands:\n"
        "/status - View your monitored channels\n"
        "/add <url> - Add a new channel\n"
        "/remove - Delete a channel\n"
        "/fetch - Scan for new videos now"
    )
    await update.message.reply_text(help_msg)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    channels = delivery.get_channels()
    if not channels:
        await update.message.reply_text("Your monitor list is empty.")
        return
    msg = "Currently Monitoring:\n\n"
    for c in channels:
        display = c.get('name') or c.get('handle', 'Unknown')
        channel_id = c.get('channel_id', 'No ID')
        msg += f"- {display} ({channel_id})\n"
    await update.message.reply_text(msg)


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if not context.args:
        await update.message.reply_text("Please provide a channel URL or handle.")
        return
    url = context.args[0]
    result = delivery.add_new_channel(url)
    if result:
        await update.message.reply_text(f"Added {result}")
    else:
        await update.message.reply_text("Could not add channel. Make sure it's a valid YouTube URL.")

async def remove_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    reply_markup = await delivery.get_remove_menu()
    if reply_markup:
        await update.message.reply_text("Select a channel to remove:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("No channels found to remove.")


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data.startswith("remove_"):
        identifier = query.data.replace("remove_", "")
        if delivery.remove_channel(identifier):
            await query.edit_message_text(text=f"Removed: {identifier}")
        else:
            await query.edit_message_text(text="Failed to remove.")


if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not set in .env")
    if not AUTHORIZED_CHAT_ID:
        raise ValueError("TELEGRAM_CHANNEL_ID not set in .env")

    application = ApplicationBuilder().token(token).build()

    pst = ZoneInfo("America/Los_Angeles")
    application.job_queue.run_daily(
        scheduled_fetch,
        time=time(hour=19, minute=0, tzinfo=pst)
    )

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("start", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("add", add_command))
    application.add_handler(CommandHandler("remove", remove_command))
    application.add_handler(CommandHandler("fetch", fetch_command))
    application.add_handler(CallbackQueryHandler(handle_callback))

    print(f"Bot started. Authorized ID: {AUTHORIZED_CHAT_ID}")
    application.run_polling()
