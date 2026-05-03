import os
import time
from dotenv import load_dotenv
from fetcher import VideoFetcher
from summarizer import VideoSummarizer
from delivery import TelegramDelivery

load_dotenv()

def main():
    # Initialize the parts of the project
    fetcher = VideoFetcher()
    summarizer = VideoSummarizer()
    delivery = TelegramDelivery()
    
    print("Starting YouTube Monitor...")

    while True:
        try:
            # 1. Fetch new videos
            new_videos = fetcher.get_new_videos()
            
            for video in new_videos:
                print(f"Processing: {video['title']}")
                
                # 2. Get the summary from your Oracle Cloud
                summary = summarizer.summarize(video['transcript'])
                
                # 3. Send to Telegram
                message = f"<b>{video['title']}</b>\n\n{summary}\n\n<a href='{video['url']}'>Watch Video</a>"
                delivery.send_message(message)
                
            # Wait 30 minutes before checking again
            time.sleep(1800)
            
        except Exception as e:
            print(f"Loop error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
