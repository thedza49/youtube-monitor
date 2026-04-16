# YouTube Monitor

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
