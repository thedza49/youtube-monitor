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

    def summarize(self, transcript_list, video_title):
        """
        Generates a structured summary using Gemini Flash.
        """
        # Format transcript for the prompt
        formatted_transcript = ""
        for entry in transcript_list:
            start = entry['start']
            minutes = int(start // 60)
            seconds = int(start % 60)
            timestamp = f"[{minutes:02d}:{seconds:02d}]"
            formatted_transcript += f"{timestamp} {entry['text']}\n"

        prompt = f"""
You are an expert video summarizer. Summarize the following YouTube video transcript.
Video Title: {video_title}

Your summary MUST follow this Markdown template:

# Summary: {video_title}

## Narrative Summary
[Provide a 3-5 paragraph narrative summary of the video content, explaining the main themes and flow.]

## Key Points
- [Key point 1]
- [Key point 2]
- ... (list at least 5 key points)

## Notable Quotes
- "[Quote text]" ([timestamp])
- ...

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
