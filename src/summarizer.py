import requests
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

class VideoSummarizer:
    def __init__(self):
        base_url = os.getenv("OLLAMA_BASE_URL", "http://129.146.37.17:11434")
        self.url = f"{base_url}/api/generate"
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

    def get_transcript(self, video_id):
        try:
            api = YouTubeTranscriptApi()
            transcript = api.fetch(video_id)
            return " ".join([entry.text for entry in transcript])
        except Exception as e:
            print(f"Transcript error for {video_id}: {type(e).__name__}: {e}")
            return None

    def summarize(self, video_id, title, channel_name, link, summary_focus):
        transcript = self.get_transcript(video_id)
        if transcript:
            prompt = (
                f"You are summarizing a YouTube video for a busy professional.\n\n"
                f"Channel: {channel_name}\n"
                f"Title: {title}\n"
                f"Focus: {summary_focus}\n\n"
                f"Transcript:\n{transcript}\n\n"
                f"Write a structured summary with:\n"
                f"## Narrative Summary\n(2-3 sentences)\n\n"
                f"## Key Points\n(bullet list)\n\n"
                f"## Actionable Takeaways\n(bullet list focused on: {summary_focus})"
            )
        else:
            prompt = (
                f"You are summarizing a YouTube video for a busy professional.\n\n"
                f"Channel: {channel_name}\n"
                f"Title: {title}\n"
                f"Focus: {summary_focus}\n\n"
                f"No transcript was available. Based on the title alone, write a brief note "
                f"explaining what this video likely covers and why it may be relevant. "
                f"Clearly label this as title-only inference."
            )
        payload = {"model": self.model, "prompt": prompt, "stream": False, "options": {"num_ctx": 32768}}
        try:
            response = requests.post(self.url, json=payload, timeout=None)
            response.raise_for_status()
            return response.json().get("response", "Summary failed.")
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"
