import google.generativeai as genai
import os
import json

class VideoSummarizer:
    def __init__(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def summarize(self, transcript_list, video_title, summary_focus="general interest", metadata=None):
        """
        Generates a structured summary using Gemini Flash.
        """
        video_id = metadata.get('video_id', 'VIDEO_ID') if metadata else 'VIDEO_ID'
        
        # Format transcript for the prompt with clickable timestamp links
        formatted_transcript = ""
        for entry in transcript_list:
            start = entry['start']
            minutes = int(start // 60)
            seconds = int(start % 60)
            timestamp_label = f"{minutes:02d}:{seconds:02d}"
            # Format: [MM:SS](https://youtu.be/ID?t=SECONDS)
            timestamp_link = f"[{timestamp_label}](https://youtu.be/{video_id}?t={int(start)})"
            formatted_transcript += f"{timestamp_link} {entry['text']}\n"

        # Prepare metadata string
        meta_str = ""
        if metadata:
            # podcast_name is used in the list below, so we don't repeat it in meta_str if we follow the structure
            # but date and guest info are good to have.
            pass

        youtube_url = metadata.get('url', 'N/A') if metadata else 'N/A'
        clickable_url = f"[{youtube_url}]({youtube_url})" if youtube_url != 'N/A' else 'N/A'

        prompt = f"""
You are an expert video summarizer. Analyze the following YouTube video transcript and metadata.
Video Title: {video_title}
Podcast Name: {metadata.get('podcast_name', 'N/A') if metadata else 'N/A'}

Identify the main guest(s) and extract a **Guest Bio** (Who they are and what they do) based on the transcript and video information.

Your summary MUST follow this structure:

# {video_title}

## Episode Metadata
- **Podcast Name:** {metadata.get('podcast_name', 'N/A') if metadata else 'N/A'}
- **YouTube URL:** {clickable_url}
- **Date Posted:** {metadata.get('date', 'N/A') if metadata else 'N/A'}
- **Guest Info:** [Extracted Guest Name and a 1-2 sentence bio about who they are and what they do]

## Overview
[Provide a brief 2-3 sentence high-level overview of the video.]

## Themes & Key Insights
Organize the content into logical thematic sections. Focus on: {summary_focus}

### [Theme 1 Name]
- [Insight/Point 1]
- [Insight/Point 2]
- [Insight/Point 3]

### [Theme 2 Name]
- [Insight/Point 1]
- [Insight/Point 2]
- ...

## Notable Quotes
- "[Quote text]" ([timestamp_link])
- ...

CRITICAL INSTRUCTION: All timestamps in your summary (especially in the Notable Quotes section) MUST be formatted exactly as they appear in the transcript: `[MM:SS](https://youtu.be/VIDEO_ID?t=SECONDS)`. Do NOT use plain text timestamps like [12:34]. Use the full Markdown link provided in the transcript.

Transcript:
{formatted_transcript}
"""
        
        response = self.model.generate_content(prompt)
        return response.text

if __name__ == "__main__":
    # Test stub
    from fetcher import TranscriptFetcher
    fetcher = TranscriptFetcher()
    transcript = fetcher.fetch("dQw4w9WgXcQ")
    if transcript:
        summarizer = VideoSummarizer()
        summary = summarizer.summarize(transcript, "Rick Astley - Never Gonna Give You Up")
        print(summary)
    else:
        print("Failed to fetch transcript for testing")
