# UAL Service Bot

A clean, fast, and aesthetic Discord bot for United Virtual Airlines to manage flights using slash commands.

## Features

- `/start_flight` - Begin logging a flight
- `/end_flight` - Submit your completed flight with screenshot
- `/stats` - See how many flights you've logged
- `/view_flight` - See your last flight log neatly

## Deployment (Railway)

1. Fork this repo or clone it locally.
2. Create a new project on [Railway](https://railway.app/).
3. Deploy from GitHub and select this repo.
4. Add your Discord Bot Token as an environment variable:
   - Key: `TOKEN`
   - Value: `your_bot_token_here`
5. Railway will install dependencies automatically and run your bot.
6. Your bot will come online and be ready to handle your VA operations.

## Requirements

- Python
- discord.py
