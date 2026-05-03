import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from delivery import DeliveryManager

# Setup
load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize Delivery Manager
delivery = DeliveryManager()

# Security: Only respond to your specific Channel ID
AUTHORIZED_CHAT_ID = os.getenv("TELEGRAM_CHANNEL_ID")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Specific help menu for the YouTube Summarizer bot."""
    if str(update.effective_chat.id) != AUTHORIZED_CHAT_ID:
        return
    
    help_msg = (
        "🤖 **@YTSum49bot | YouTube Summarizer**\n\n"
        "This bot monitors your configured YouTube channels and posts AI-generated summaries.\n\n"
        "**Available Commands:**\n"
        "• `/status` - View your currently monitored YouTube channels\n"
        "• `/add <url>` - Add a new channel (e.g., `/add https://youtube.com/@TheCompound`)\n"
        "• `/remove` - Open the interactive menu to delete a channel\n"
        "• `/fetch` - Manually check for new videos right now"
    )
    await update.message.reply_text(help_msg, parse_mode="Markdown")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lists the channels currently being monitored."""
    if str(update.effective_chat.id) != AUTHORIZED_CHAT_ID:
        return
    
    channels = delivery.get_channels()
    if not channels:
        await update.message.reply_text("Your monitor list is currently empty.")
        return
    
    msg = "📺 **Currently Monitoring:**\n\n"
    for c in channels:
        msg += f"• {c['name']} ({c['url']})\n"
    
    await update.message.reply_text(msg, parse_mode="Markdown")

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Adds a new YouTube channel to the YAML config."""
    if str(update.effective_chat.id) != AUTHORIZED_CHAT_ID:
        return

    if not context.args:
        await update.message.reply_text("❌ Please provide a URL.\nExample: `/add https://youtube.com/@TheCompound`", parse_mode="Markdown")
        return

    url = context.args[0]
    try:
        name = delivery.add_new_channel(url)
        await update.message.reply_text(f"✅ Added **{name}** to the monitor list.", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

async def remove_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows an interactive menu to delete channels."""
    if str(update.effective_chat.id) != AUTHORIZED_CHAT_ID:
        return

    reply_markup = await delivery.get_remove_menu()
    if reply_markup:
        await update.message.reply_text("Select a channel to remove:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("No channels found to remove.")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes the 'Remove' button clicks."""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("remove_"):
        channel_name = query.data.replace("remove_", "")
        if delivery.remove_channel(channel_name):
            await query.edit_message_text(text=f"🗑 Removed: {channel_name}")

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    application = ApplicationBuilder().token(token).build()
    
    # Registering all commands
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("start", help_command)) # Start shows help too
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("add", add_command))
    application.add_handler(CommandHandler("remove", remove_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    print("Bot is listening for / commands...")
    application.run_polling()
