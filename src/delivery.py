import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TelegramDelivery:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def send_message(self, text):
        if not self.token or not self.chat_id:
            print("Telegram credentials missing in .env")
            return
            
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            print("Message sent to Telegram!")
        except Exception as e:
            print(f"Failed to send Telegram message: {e}")
