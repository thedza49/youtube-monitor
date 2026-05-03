import yaml
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class DeliveryManager:
    def __init__(self, channels_file="config/channels.yaml"):
        self.channels_file = channels_file

    def get_channels(self):
        if not os.path.exists(self.channels_file):
            return []
        try:
            with open(self.channels_file, 'r') as f:
                data = yaml.safe_load(f)
                return data.get('channels', []) if data else []
        except Exception:
            return []

    async def get_remove_menu(self):
        channels = self.get_channels()
        if not channels:
            return None
            
        keyboard = []
        for c in channels:
            # FLEXIBLE LOGIC: Check for 'name' first, then 'handle', then 'url'
            display_name = c.get('name') or c.get('handle') or c.get('url', 'Unknown')
            # Use the same logic for the callback value
            callback_val = c.get('name') or c.get('handle') or "unknown"
            
            keyboard.append([InlineKeyboardButton(f"❌ {display_name}", callback_data=f"remove_{callback_val}")])
            
        return InlineKeyboardMarkup(keyboard)

    def remove_channel(self, identifier):
        channels = self.get_channels()
        # Filter matching against name, handle, or url
        updated = [c for c in channels if c.get('name') != identifier and 
                   c.get('handle') != identifier and 
                   c.get('url') != identifier]
        
        if len(channels) == len(updated):
            return False
            
        with open(self.channels_file, 'w') as f:
            yaml.safe_dump({"channels": updated}, f)
        return True
