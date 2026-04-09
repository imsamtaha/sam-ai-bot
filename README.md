# Sam AI Bot

An AI-powered Telegram bot built with Google Gemini AI and Polygon DeFi integration.

## Features

- 🤖 **Google Gemini AI Integration** - Chat with advanced AI for insights and assistance
- 📊 **Crypto Market Analysis** - Get AI-powered market analysis
- 💡 **Trading Advice** - Receive educational trading information
- 💼 **Wallet Integration** - Connect your Polygon wallet (coming soon)
- 🏦 **DeFi Operations** - Swap tokens and manage DeFi activities (coming soon)

## Setup

### Prerequisites

- Python 3.9+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Google Gemini API Key (from [Google AI Studio](https://ai.google.dev/))

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/imsamtaha/sam-ai-bot.git
   cd sam-ai-bot
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Running the Bot

**Polling Mode (Development):**
```bash
python main.py
```

**Webhook Mode (Production):**
```bash
USE_WEBHOOK=true python main.py
```

Or run just the Telegram bot:
```bash
python -m app.telegram_bot
```

## Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/help` | Show help message |
| `/ai <message>` | Chat with Gemini AI |
| `/market` | Get crypto market analysis |
| `/advice [crypto]` | Get trading advice |
| `/wallet` | Check your wallet |
| `/defi` | DeFi operations |

## API Endpoints

When running in webhook mode, the following endpoints are available:

- `GET /` - Health check
- `GET /health` - Health status
- `POST /webhook` - Telegram webhook endpoint
- `POST /ai/chat` - Chat with AI
- `GET /ai/market` - Market analysis
- `POST /ai/advice` - Trading advice
- `GET /metrics` - Performance metrics (request counts, response times, error rates)

## Project Structure

```
sam-ai-bot/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── app/
│   ├── __init__.py
│   ├── routes.py        # FastAPI routes
│   └── telegram_bot.py  # Telegram bot handlers
└── services/
    ├── __init__.py
    ├── ai_chat.py       # Google Gemini AI integration
    └── metrics.py       # Performance metrics tracking
```

## License

MIT License