from youtube_transcript_api import YouTubeTranscriptApi
import os

class TranscriptFetcher:
    def fetch(self, video_id):
        """
        Fetches the transcript for a given video ID and returns it as a list of dicts.
        """
        try:
            api = YouTubeTranscriptApi()
            transcript_obj = api.fetch(video_id)
            # Convert to list of dicts for compatibility
            return [{'text': entry.text, 'start': entry.start, 'duration': entry.duration} for entry in transcript_obj]
        except Exception as e:
            print(f"Error fetching transcript for {video_id}: {e}")
            return None

    def get_full_text(self, transcript_list):
        if not transcript_list:
            return ""
        return " ".join([entry['text'] for entry in transcript_list])

if __name__ == "__main__":
    fetcher = TranscriptFetcher()
    transcript = fetcher.fetch("dQw4w9WgXcQ")
    if transcript:
        full_text = fetcher.get_full_text(transcript)
        print("Successfully fetched transcript (first 100 chars):")
        print(full_text[:100] + "...")
    else:
        print("Failed to fetch transcript")
