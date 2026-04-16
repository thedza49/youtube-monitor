🧠 Brain Source: Gemini

# Implementation Plan: YouTube Monitor (v1.0.0)

## Overview
A native Python monitor for the Raspberry Pi that tracks YouTube channels via RSS, summarizes transcripts using the Oracle VM LLM, and delivers PDF reports via Telegram.

## Architecture & Risks
- **Core:** Python + `feedparser` + `youtube-transcript-api`.
- **PDF Generation:** Using `weasyprint` or `mdpdf`. 
- **⚠️ ARM Risk:** PDF libraries like `weasyprint` have heavy C-dependencies (`pango`, `cairo`). We will verify these on the Pi 4 before proceeding.
- **Delivery:** OpenClaw CLI for direct Telegram routing.

## Phase 1: Foundation (Momo)
- [ ] **Task 1: Project Structure.** Initialize `projects/youtube-monitor` with `src/`, `config/`, and `data/` directories.
- [ ] **Task 2: Config Schema.** Create `config/channels.yaml` with support for `channel_id`, `keywords`, and `max_age`.
- [ ] **Task 3: State Management.** Implement `data/seen_videos.json` to prevent duplicates.

## Phase 2: Core Engine (Momo)
- [ ] **Task 4: RSS Poller.** Implement `poller.py` using `feedparser` to extract video IDs from channel RSS feeds.
- [ ] **Task 5: Transcript Fetcher.** Integrate `youtube-transcript-api` to pull raw captions.
- [ ] **Task 6: LLM Integration.** Create `summarizer.py` to send transcripts to the Oracle VM LLM endpoint with a structured prompt.

## Phase 3: Output & Delivery (Momo)
- [ ] **Task 7: PDF Generation.** Install dependencies and implement `pdf_gen.py`. Verify ARM compatibility.
- [ ] **Task 8: Telegram Bridge.** Implement delivery logic using `openclaw message send`.

## Phase 4: Automation (Momo)
- [ ] **Task 9: systemd Service.** Create and enable `youtube-monitor.service` to run daily.

## Verification (Larry)
- [ ] Verify RSS polling logic.
- [ ] Confirm PDF renders correctly on Pi 4.
- [ ] Validate Telegram delivery with a test video.
