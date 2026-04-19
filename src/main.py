import os
import sys
from poller import YouTubePoller
from fetcher import TranscriptFetcher
from summarizer import VideoSummarizer
from pdf_gen import PDFGenerator
from delivery import TelegramDeliverer
import time

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, 'config', 'channels.yaml')
    seen_videos_path = os.path.join(base_dir, 'data', 'seen_videos.json')
    output_dir = os.path.join(base_dir, 'data', 'summaries')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    poller = YouTubePoller(config_path, seen_videos_path)
    fetcher = TranscriptFetcher()
    summarizer = VideoSummarizer()
    pdf_gen = PDFGenerator()
    deliverer = TelegramDeliverer()

    print("Polling for new videos...")
    new_videos = poller.poll()
    print(f"Found {len(new_videos)} new videos.")

    for video in new_videos:
        video_id = video['id']
        title = video['title']
        print(f"Processing: {title} ({video_id})")

        # 1. Fetch transcript
        transcript = fetcher.fetch(video_id)
        if not transcript:
            print(f"Skipping {video_id}: No transcript available.")
            continue

        # 2. Summarize
        print("Generating summary...")
        try:
            summary_focus = video.get('summary_focus', 'general interest')
            metadata = {
                'podcast_name': video.get('channel_name'),
                'url': video.get('link'),
                'date': video.get('published'),
                'video_id': video_id
            }
            summary_md = summarizer.summarize(transcript, title, summary_focus, metadata)
        except Exception as e:
            print(f"Error summarizing {video_id}: {e}")
            continue

        # 3. Generate PDF
        pdf_filename = f"{video_id}_summary.pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)
        print(f"Generating PDF: {pdf_path}")
        pdf_gen.generate(summary_md, pdf_path)

        # 4. Deliver
        print("Delivering to Telegram...")
        caption = f"Summary for: {title}\n{video['link']}"
        success = deliverer.deliver(pdf_path, caption)

        if success:
            # 5. Mark as seen
            poller.seen_videos.append(video_id)
            poller.save_seen_videos(poller.seen_videos)
            print(f"Finished processing {video_id}")
        else:
            print(f"Failed to deliver {video_id}, not marking as seen.")

if __name__ == "__main__":
    main()
