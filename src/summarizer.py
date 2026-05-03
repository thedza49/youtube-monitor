import requests
import os
from dotenv import load_dotenv

load_dotenv()

class VideoSummarizer:
    def __init__(self):
        # This looks at your Pi's .env file for the Oracle IP
        base_url = os.getenv("OLLAMA_BASE_URL", "http://129.146.37.17:11434")
        self.url = f"{base_url}/api/generate"
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:3b")

    def summarize(self, text):
        if not text:
            return "No transcript available."
            
        prompt = f"Summarize this YouTube transcript into a clear, bulleted list:\n\n{text}"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            # We give it 120 seconds because LLMs take a moment to 'think'
            response = requests.post(self.url, json=payload, timeout=120)
            response.raise_for_status()
            return response.json().get('response', 'Summary failed.')
        except Exception as e:
            return f"Error connecting to Oracle/Ollama: {str(e)}"
