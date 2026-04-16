import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import json
from datetime import datetime, timezone, timedelta

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from poller import YouTubePoller
from fetcher import TranscriptFetcher

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.base_dir, 'config', 'channels.yaml')
        self.data_path = os.path.join(self.base_dir, 'data', 'test_seen_videos.json')
        
        # Ensure test data file is clean
        with open(self.data_path, 'w') as f:
            json.dump([], f)

    def tearDown(self):
        if os.path.exists(self.data_path):
            os.remove(self.data_path)

    @patch('feedparser.parse')
    def test_poller_filters_new_videos(self, mock_parse):
        # Mock RSS response
        now = datetime.now(timezone.utc)
        
        def create_entry(vid, title, published_time):
            e = MagicMock()
            e.yt_videoid = vid
            e.title = title
            e.link = f"https://youtube.com/watch?v={vid}"
            e.published = published_time.isoformat()
            e.published_parsed = None
            # Handle .get() calls for keywords and published
            e.get.side_effect = lambda k, d=None: getattr(e, k, d)
            return e

        # Entry 1: New, matches keyword
        e1 = create_entry("vid1", "TCAF Episode 1", now)
        
        # Entry 2: New, does NOT match keyword
        e2 = create_entry("vid2", "Random Vlog", now)
        
        # Entry 3: Already seen, matches keyword
        e3 = create_entry("seen_vid", "TCAF Episode 0", now)
        
        # Entry 4: Too old, matches keyword
        e4 = create_entry("old_vid", "TCAF Ancient", now - timedelta(days=10))

        mock_feed = MagicMock()
        mock_feed.entries = [e1, e2, e3, e4]
        mock_parse.return_value = mock_feed
        
        # Pre-populate seen_videos
        with open(self.data_path, 'w') as f:
            json.dump(["seen_vid"], f)
            
        poller = YouTubePoller(self.config_path, self.data_path)
        new_videos = poller.poll()
        
        # Should only find vid1
        self.assertEqual(len(new_videos), 1, f"Expected 1 video, got {[v['id'] for v in new_videos]}")
        self.assertEqual(new_videos[0]['id'], "vid1")

    @patch('youtube_transcript_api.YouTubeTranscriptApi.fetch')
    def test_fetcher_returns_raw_text(self, mock_fetch):
        # Mocking the new object-based return
        m1 = MagicMock()
        m1.text = 'Hello'
        m2 = MagicMock()
        m2.text = 'world'
        mock_fetch.return_value = [m1, m2]
        
        fetcher = TranscriptFetcher()
        text = fetcher.fetch("test_id")
        
        self.assertEqual(text, "Hello world")

if __name__ == '__main__':
    unittest.main()
