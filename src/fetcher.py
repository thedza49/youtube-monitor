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
            channels_data = yaml.safe_load(f)

        processed_ids = []
        if os.path.exists(self.processed_file):
            with open(self.processed_file, 'r') as f:
                processed_ids = f.read().splitlines()

        new_videos = []
        # Extract the list of channels from the YAML structure
        channels_list = channels_data.get('channels', [])
        
        for channel in channels_list:
            # Get the ID from the dictionary entry
            channel_id = channel.get('id')
            if not channel_id:
                continue

            rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries:
                if entry.id not in processed_ids:
                    print(f"Found new video: {entry.title}")
                    new_videos.append({
                        'title': entry.title,
                        'url': entry.link,
                        'transcript': f"Title: {entry.title}. Link: {entry.link}",
                        'id': entry.id
                    })
                    # Add to processed list so we don't double-post
                    with open(self.processed_file, 'a') as f:
                        f.write(entry.id + "\n")
        
        return new_videos
