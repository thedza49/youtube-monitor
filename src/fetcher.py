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
        # Fixed logic: Loop through the list and grab just the 'id'
        for channel in channels_data.get('channels', []):
            channel_id = channel.get('id')
            if not channel_id:
                continue

            rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries:
                if entry.id not in processed_ids:
                    new_videos.append({
                        'title': entry.title,
                        'url': entry.link,
                        'transcript': f"Title: {entry.title}. Link: {entry.link}",
                        'id': entry.id
                    })
                    with open(self.processed_file, 'a') as f:
                        f.write(entry.id + "\n")
        
        return new_videos
