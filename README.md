# YouTube Monitor Bot

A dedicated Telegram bot that monitors YouTube channels, fetches new videos, and posts AI-generated summaries to a specific Telegram channel.

## 🛠 Features
- **Dedicated Bot**: Scoped specifically to `@YTSum49bot`.
- **Command Control**: Manage your monitor list via `/add`, `/remove`, and `/status`.
- **Security**: "Gatekeeper" logic ensures the bot only responds in the authorized channel.
- **YAML Config**: All monitored channels are stored in `config/channels.yaml`.

## 🚀 Commands
- `/help`: Shows the YouTube-specific help menu.
- `/status`: Lists all currently monitored channels.
- `/add <url>`: Adds a new YouTube channel to the monitor list.
- `/remove`: Opens an interactive menu to delete a channel.
- `/fetch`: Manually triggers a scan for new videos.

## 📂 Project Structure
- `src/main.py`: The entry point and Telegram command handler.
- `src/delivery.py`: Logic for managing the channel list and interactive menus.
- `config/channels.yaml`: The data store for your monitored URLs.
- `.env`: (Local Only) Contains private API keys and IDs.

## 🔄 Workflow
1. Update code on GitHub.
2. On Raspberry Pi: `git fetch origin && git reset --hard origin/master`.
3. Restart: `python3 src/main.py`.
