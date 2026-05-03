def get_new_videos(self):
        # Force the path to be absolute so there is no confusion
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.processed_file = os.path.join(base_dir, "processed_videos.txt")
        self.channels_file = os.path.join(base_dir, "channels.yaml")

        if not os.path.exists(self.channels_file):
            print(f"Error: {self.channels_file} not found!")
            return []

        with open(self.channels_file, 'r') as f:
            channels_data = yaml.safe_load(f)

        processed_ids = []
        if os.path.exists(self.processed_file):
            with open(self.processed_file, 'r') as f:
                processed_ids = f.read().splitlines()
        
        print(f"DEBUG: Memory file has {len(processed_ids)} videos stored.")

        new_videos = []
        for channel in channels_data.get('channels', []):
            channel_id = channel.get('id')
            print(f"Checking: {channel.get('name')} ({channel_id})...")
            
            rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries:
                if entry.id not in processed_ids:
                    print(f"Found NEW video: {entry.title}")
                    new_videos.append({
                        'title': entry.title,
                        'url': entry.link,
                        'transcript': f"Title: {entry.title}. Link: {entry.link}",
                        'id': entry.id
                    })
                    with open(self.processed_file, 'a') as f:
                        f.write(entry.id + "\n")
                else:
                    # This tells us it's working even if there are no new videos
                    pass 
        
        return new_videos
