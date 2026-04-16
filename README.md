## Important Operational Rules
- **No Mass Summarization:** This tool is strictly for forward-looking monitoring. 
- **Backlog Handling:** Upon subscribing to a new channel, the `seen_videos.json` must be pre-populated with the channel's current top 50 videos to prevent the system from attempting to summarize historical content.
- **Safety Valve:** The systemd service is configured to process new releases only. Any manual runs should be restricted to specific video IDs to avoid flooding.

Automatically polls YouTube channels for new videos, fetches transcripts, generates summaries using AI, and delivers them as PDFs via Telegram.

## Setup

1. **Environment**:
   - Python 3.11+
   - Create a virtual environment: `python -m venv venv`
   - Install dependencies: `./venv/bin/pip install -r requirements.txt`

2. **Configuration**:
   - Edit `config/channels.yaml` to add your target channels.
   - Ensure environment variables are set (e.g., `GOOGLE_API_KEY` for Gemini, `TELEGRAM_TARGET`).

3. **Running**:
   - Run manually: `./venv/bin/python src/main.py`
   - Or install as a systemd service (see `config/youtube-monitor.service`).

## Automation

The project includes a systemd user service template for daily monitoring.
