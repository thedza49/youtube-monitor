import yaml
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class DeliveryManager:
    def __init__(self, channels_file="config/channels.yaml"):
        self.channels_file = channels_file

    def get_channels(self):
        """Loads channels from the YAML file."""
        if not os.path.exists(self.channels_file):
            return []
        with open(self.channels_file, 'r') as f:
            data = yaml.safe_load(f)
            return data.get('channels', [])

    def add_new_channel(self, url):
        """Appends a new channel to the YAML file."""
        channels = self.get_channels()
        
        # Simple name extraction from the URL
        clean_name = url.split("@")[-1] if "@" in url else url.split("/")[-1]
        
        new_entry = {
            "name": clean_name,
            "url": url,
            "summary_focus": "General summary of key points"
        }
        
        channels.append(new_entry)
        
        with open(self.channels_file, 'w') as f:
            yaml.safe_dump({"channels": channels}, f)
            
        return clean_name

    def remove_channel(self, name):
        """Deletes a channel by name."""
        channels = self.get_channels()
        updated_channels = [c for c in channels if c['name'] != name]
        
        if len(channels) == len(updated_channels):
            return False
            
        with open(self.channels_file, 'w') as f:
            yaml.safe_dump({"channels": updated_channels}, f)
        return True

    async def get_remove_menu(self):
        """Creates the interactive button menu for deletion."""
        channels = self.get_channels()
        if not channels:
            return None
            
        keyboard = []
        for c in channels:
            keyboard.append([InlineKeyboardButton(f"❌ {c['name']}", callback_data=f"remove_{c['name']}")])
            
        return InlineKeyboardMarkup(keyboard)
