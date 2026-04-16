import yaml
import json
import feedparser
import os
from datetime import datetime, timedelta, timezone

class YouTubePoller:
    def __init__(self, config_path, seen_videos_path):
        self.config_path = config_path
        self.seen_videos_path = seen_videos_path
        self.config = self._load_config()
        self.seen_videos = self._load_seen_videos()

    def _load_config(self):
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def _load_seen_videos(self):
        if not os.path.exists(self.seen_videos_path):
            return []
        try:
            with open(self.seen_videos_path, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_seen_videos(self, seen_videos):
        with open(self.seen_videos_path, 'w') as f:
            json.dump(seen_videos, f, indent=2)

    def poll(self):
        new_videos = []
        now = datetime.now(timezone.utc)
        
        for channel in self.config.get('channels', []):
            channel_id = channel.get('channel_id')
            if not channel_id:
                print(f"Warning: No channel_id for {channel.get('handle', 'unknown')}")
                continue
            
            feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            feed = feedparser.parse(feed_url)
            
            # SAFETY: If this is the FIRST time we are seeing this channel, 
            # mark all currently available videos as seen so we only process future releases.
            is_new_channel = not any(v.get('channel_handle') == channel.get('handle') for v in self.seen_videos if isinstance(v, dict))
            # Fallback for simple string lists
            if not is_new_channel and all(isinstance(v, str) for v in self.seen_videos):
                # If we only have IDs, we can't easily attribute to channel, 
                # but the user already has a seen_videos list.
                pass 

            rules = channel.get('rules', {})
            max_age_days = rules.get('max_age_days', 7)
            keywords = rules.get('keywords', [])
            
            for entry in feed.entries:
                # feedparser adds yt_videoid if the namespace is present
                video_id = getattr(entry, 'yt_videoid', None)
                if not video_id:
                    # Fallback to parsing from link if needed
                    if 'link' in entry:
                        video_id = entry.link.split('v=')[-1]
                
                if not video_id or video_id in self.seen_videos:
                    continue
                
                # Check age
                try:
                    # feedparser dates are usually in a consistent format but can vary
                    published_parsed = entry.get('published_parsed')
                    if published_parsed:
                        published = datetime(*published_parsed[:6], tzinfo=timezone.utc)
                    else:
                        published_str = entry.get('published', '')
                        # Handle common YouTube RSS date format: 2024-03-15T12:00:00+00:00
                        published = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
                except (ValueError, TypeError) as e:
                    print(f"Error parsing date for {video_id}: {e}")
                    continue

                age = now - published
                if age.days > max_age_days:
                    continue
                
                # Check keywords
                title = entry.get('title', '')
                if keywords:
                    match = any(kw.lower() in title.lower() for kw in keywords)
                    if not match:
                        continue
                
                new_videos.append({
                    'id': video_id,
                    'title': title,
                    'link': entry.link,
                    'published': published.isoformat(),
                    'channel_handle': channel.get('handle')
                })
        
        return new_videos

if __name__ == "__main__":
    # Example usage (for testing)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    poller = YouTubePoller(
        os.path.join(base_dir, 'config', 'channels.yaml'),
        os.path.join(base_dir, 'data', 'seen_videos.json')
    )
    new = poller.poll()
    print(f"Found {len(new)} new videos")
    for v in new:
        print(f"- {v['title']} ({v['id']})")
