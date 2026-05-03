import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from delivery import DeliveryManager

# Setup
load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

delivery = DeliveryManager()
AUTHORIZED_CHAT_ID = os.getenv("TELEGRAM_CHANNEL_ID")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_id = str(update.effective_chat.id)
    print(f"DEBUG: Received command from ID: {current_id}") # This helps us see why it's silent
    
    if current_id != AUTHORIZED_CHAT_ID:
        print(f"DEBUG: ID {current_id} does not match AUTHORIZED_CHAT_ID {AUTHORIZED_CHAT_ID}")
        return
    
    help_msg = (
        "🤖 **@YTSum49bot | YouTube Summarizer**\n\n"
        "This bot monitors your configured YouTube channels.\n\n"
        "**Available Commands:**\n"
        "• `/status` - View your monitored channels\n"
        "• `/add <url>` - Add a new channel\n"
        "• `/remove` - Delete a channel\n"
        "• `/fetch` - Scan for new videos"
    )
    await update.message.reply_text(help_msg, parse_mode="Markdown")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != AUTHORIZED_CHAT_ID:
        return
    channels = delivery.get_channels()
    msg = "📺 **Currently Monitoring:**\n\n" + "\n".join([f"• {c['name']} ({c['url']})" for c in channels]) if channels else "Your list is empty."
    await update.message.reply_text(msg, parse_mode="Markdown")

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != AUTHORIZED_CHAT_ID:
        return
    if not context.args:
        await update.message.reply_text("❌ Use: `/add <url>`")
        return
    url = context.args[0]
    name = delivery.add_new_channel(url)
    await update.message.reply_text(f"✅ Added **{name}**")

async def remove_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != AUTHORIZED_CHAT_ID:
        return
    reply_markup = await delivery.get_remove_menu()
    await update.message.reply_text("Select a channel to remove:", reply_markup=reply_markup) if reply_markup else await update.message.reply_text("No channels found.")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data.startswith("remove_"):
        channel_name = query.data.replace("remove_", "")
        if delivery.remove_channel(channel_name):
            await query.edit_message_text(text=f"🗑 Removed: {channel_name}")

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("start", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("add", add_command))
    application.add_handler(CommandHandler("remove", remove_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    print(f"Bot started. Authorized ID is: {AUTHORIZED_CHAT_ID}")
    application.run_polling()
