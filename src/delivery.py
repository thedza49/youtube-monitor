import subprocess
import os

class TelegramDeliverer:
    def __init__(self, target=None):
        self.target = target or os.environ.get("TELEGRAM_TARGET", "daniel")

    def deliver(self, file_path, caption=""):
        """
        Delivers the file to Daniel on Telegram using OpenClaw CLI.
        """
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return False

        try:
            cmd = [
                "openclaw", "message", "send",
                "--channel", "telegram",
                "--target", self.target,
                "--media", file_path
            ]
            if caption:
                cmd.extend(["--message", caption])
            
            print(f"Executing: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Successfully delivered via Telegram")
                return True
            else:
                print(f"Error delivering via Telegram: {result.stderr}")
                return False
        except Exception as e:
            print(f"Exception during delivery: {e}")
            return False

if __name__ == "__main__":
    # Test stub (requires a real file)
    deliverer = TelegramDeliverer()
    # deliverer.deliver("test_summary.pdf", "Here is your test summary")
