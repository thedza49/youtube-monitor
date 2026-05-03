import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import yaml

class DeliveryManager:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        # Path to the channels file to allow for /remove updates
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.channels_file = os.path.join(base_dir, "config", "channels.yaml")

    async def get_remove_menu(self):
        """Generates the list of buttons for the /remove command."""
        if not os.path.exists(self.channels_file):
            return None

        with open(self.channels_file, 'r') as f:
            data = yaml.safe_load(f)
        
        channels = data.get('channels', [])
        if not channels:
            return None

        keyboard = []
        for index, channel in enumerate(channels):
            name = channel.get('handle') or channel.get('name', 'Unknown')
            # The 'callback_data' is what the bot sees when you click the button
            keyboard.append([InlineKeyboardButton(f"❌ {name}", callback_data=f"remove_{index}")])
        
        return InlineKeyboardMarkup(keyboard)

    def remove_channel_by_index(self, index):
        """Removes the channel from the YAML file."""
        with open(self.channels_file, 'r') as f:
            data = yaml.safe_load(f)
        
        removed_name = data['channels'][index].get('handle', 'Channel')
        del data['channels'][index]
        
        with open(self.channels_file, 'w') as f:
            yaml.safe_dump(data, f)
            
        return removed_name
