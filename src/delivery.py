import os
import requests

class TelegramDeliverer:
    def __init__(self):
        self.token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        self.thread_id = os.environ.get("TELEGRAM_THREAD_ID")

    def deliver(self, file_path, caption=""):
        """
        Delivers the file using the dedicated bot API.
        """
        if not self.token or not self.chat_id:
            print("Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set in .env")
            return False

        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return False

        url = f"https://api.telegram.org/bot{self.token}/sendDocument"
        
        try:
            with open(file_path, 'rb') as f:
                data = {
                    "chat_id": self.chat_id,
                    "caption": caption
                }
                if self.thread_id:
                    data["message_thread_id"] = self.thread_id
                
                files = {
                    "document": f
                }
                
                print(f"Delivering via Bot API to Chat {self.chat_id} (Thread {self.thread_id})...")
                response = requests.post(url, data=data, files=files)
                
            if response.status_code == 200:
                print("Successfully delivered via Bot API")
                return True
            else:
                print(f"Error delivering via Bot API: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"Exception during delivery: {e}")
            return False

if __name__ == "__main__":
    # Test stub (requires a real file and .env loaded)
    from dotenv import load_dotenv
    load_dotenv()
    deliverer = TelegramDeliverer()
    # deliverer.deliver("path/to/test.pdf", "Test caption")
