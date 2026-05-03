import feedparser
import yaml
import os

class VideoFetcher:
    def __init__(self):
        self.channels_file = "channels.yaml"
        self.processed_file = "processed_videos.txt"

    def get_new_videos(self):
        if not os.path.exists(self.channels_file):
            print("channels.yaml not found!")
            return []

        with open(self.channels_file, 'r') as f:
            channels = yaml.safe_load(f)

        # Load IDs of videos we've already handled
        processed_ids = []
        if os.path.exists(self.processed_file):
            with open(self.processed_file, 'r') as f:
                processed_ids = f.read().splitlines()

        new_videos = []
        for channel_id in channels.get('channels', []):
            # YouTube's RSS URL format
            rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries:
                if entry.id not in processed_ids:
                    # Collect details for the summarizer
                    new_videos.append({
                        'title': entry.title,
                        'url': entry.link,
                        'transcript': f"Title: {entry.title}. Link: {entry.link}", # Placeholder until we add full transcript logic
                        'id': entry.id
                    })
                    # Mark as processed immediately
                    with open(self.processed_file, 'a') as f:
                        f.write(entry.id + "\n")
        
        return new_videos
