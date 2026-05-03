# YouTube Monitor Bot

A dedicated Telegram bot (@YTSum49bot) that monitors YouTube channels and posts AI-generated summaries.

## 🛠 Features
- **Dockerized**: Runs in an isolated container for stability.
- **Dedicated Bot**: Scoped specifically to your YouTube project.
- **Security**: Authorized via `TELEGRAM_CHANNEL_ID` in `.env`.

## 🚀 Commands
- `/help`: Shows the YouTube-specific help menu.
- `/status`: Lists all currently monitored YouTube channels.
- `/add <url>`: Adds a new channel to the list.
- `/remove`: Opens an interactive menu to delete a channel.

## 📦 Running with Docker
1. Update code on GitHub.
2. On Pi: `git pull`.
3. Restart: `docker compose up -d --build`.

## 📂 Data Management
- `config/channels.yaml`: Stores your monitor list.
- `.env`: Local credentials (Token, Channel ID, etc.).
