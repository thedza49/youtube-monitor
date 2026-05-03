import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from delivery import DeliveryManager
from dotenv import load_dotenv

# Load environment variables (Bot Token, etc.)
load_dotenv()

# Setup logging so we can see what's happening in the terminal
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

delivery = DeliveryManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message."""
    await update.message.reply_text("YouTube Monitor Active. Use /fetch to scan or /remove to manage channels.")

async def remove_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Triggered by /remove - shows the button menu."""
    reply_markup = await delivery.get_remove_menu()
    if reply_markup:
        await update.message.reply_text("Select a channel to remove:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("No channels found in your list.")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Triggered when you tap a button."""
    query = update.callback_query
    await query.answer() # Stops the loading spinner on Telegram
    
    # Check if the button click starts with 'remove_'
    if query.data.startswith("remove_"):
        index = int(query.data.split("_")[1])
        removed_name = delivery.remove_channel_by_index(index)
        await query.edit_message_text(text=f"Successfully removed: {removed_name}")

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not found in .env file.")
    else:
        # Build the application
        application = ApplicationBuilder().token(token).build()
        
        # Register the commands
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("remove", remove_command))
        
        # Register the button click handler
        application.add_handler(CallbackQueryHandler(handle_callback))
        
        print("Bot is listening for commands...")
        application.run_polling()
