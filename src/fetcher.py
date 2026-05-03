import feedparser
import yaml
import os

class VideoFetcher:
    def __init__(self):
        # The paths are determined dynamically in get_new_videos
        pass

    def get_new_videos(self):
        # This locates the project root folder (youtube-monitor/)
        # so it can find the .yaml and .txt files correctly.
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.processed_file = os.path.join(base_dir, "processed_videos.txt")
        self.channels_file = os.path.join(base_dir, "channels.yaml")

        # 1. Check if channels.yaml exists
        if not os.path.exists(self.channels_file):
            print(f"Error: {self.channels_file} not found!")
            return []

        # 2. Load the channels we want to watch
        with open(self.channels_file, 'r') as f:
            channels_data = yaml.safe_load(f)

        # 3. Load IDs of videos we've already processed
        processed_ids = []
        if os.path.exists(self.processed_file):
            with open(self.processed_file, 'r') as f:
                processed_ids = f.read().splitlines()
        
        print(f"DEBUG: Memory file has {len(processed_ids)} videos stored.")

        new_videos = []
        
        # 4. Loop through each channel and check for new content
        for channel in channels_data.get('channels', []):
            channel_id = channel.get('id')
            channel_name = channel.get('name', 'Unknown')
            
            print(f"Checking: {channel_name}...")
            
            rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            feed = feedparser.parse(rss_url)
            
            if not feed.entries:
                print(f"   ! No videos found for {channel_name}. Check the Channel ID.")
                continue

            for entry in feed.entries:
                # If the video ID is NOT in our text file, it's new!
                if entry.id not in processed_ids:
                    print(f"   + Found NEW video: {entry.title}")
                    new_videos.append({
                        'title': entry.title,
                        'url': entry.link,
                        'transcript': f"Title: {entry.title}. Link: {entry.link}",
                        'id': entry.id
                    })
                    
                    # Add this ID to our "Memory" file immediately
                    with open(self.processed_file, 'a') as f:
                        f.write(entry.id + "\n")
        
        return new_videos
