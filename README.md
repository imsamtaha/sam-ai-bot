# Sam AI Bot

An AI-driven blockchain automation ecosystem built on Telegram, powered by Google Gemini AI and Polygon DeFi.

## Features

- 🤖 **Google Gemini AI Integration** — Chat with advanced AI for insights and assistance
- 📊 **Crypto Market Analysis** — AI-powered market analysis
- 💡 **Trading Advice** — Educational trading information
- 💼 **Wallet Portfolio** — View on-chain balances on Polygon (MATIC + ERC-20 tokens)
- 📈 **AI Portfolio Analysis** — Gemini-powered analysis of any Polygon wallet
- 🔄 **Swap Guidance** — AI explanation of token swaps across Polygon DEXs
- 🏦 **DeFi Protocols** — Information on QuickSwap, Aave, Uniswap v3, Curve, Balancer and more
- 🧠 **DeFi Strategy** — AI-generated strategy tailored to your risk profile
- ⚙️ **Blockchain Automation** — Natural-language task planning (e.g. "stake my MATIC")
- 🌐 **Network Status** — Live Polygon network and gas-price info

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
| `/advice [crypto]` | Get educational trading information |
| `/wallet <address>` | View Polygon wallet portfolio |
| `/portfolio <address>` | AI analysis of a wallet |
| `/network` | Polygon network status |
| `/defi` | List DeFi protocols on Polygon |
| `/swap <amount> <FROM> <TO>` | AI swap guidance |
| `/strategy [risk]` | AI DeFi strategy (conservative/moderate/aggressive) |
| `/automate <task>` | AI-powered blockchain automation plan |

## API Endpoints

When running in webhook mode the following endpoints are available:

### General
- `GET /` — Health check
- `GET /health` — Health status
- `POST /webhook` — Telegram webhook endpoint

### AI
- `POST /ai/chat` — Chat with Gemini AI
- `GET /ai/market` — Market analysis
- `POST /ai/advice` — Trading advice

### Blockchain
- `GET /blockchain/network` — Polygon network status
- `GET /blockchain/wallet/{address}` — On-chain portfolio
- `POST /blockchain/portfolio/analyze` — AI portfolio analysis

### DeFi
- `GET /defi/protocols` — List DeFi protocols
- `POST /defi/swap` — Swap guidance
- `POST /defi/strategy` — DeFi strategy
- `POST /defi/automate` — Blockchain automation plan

## Project Structure

```
sam-ai-bot/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── app/
│   ├── __init__.py
│   ├── routes.py        # FastAPI routes (AI + Blockchain + DeFi)
│   └── telegram_bot.py  # Telegram bot handlers
└── services/
    ├── __init__.py
    ├── ai_chat.py        # Google Gemini AI integration
    ├── blockchain.py     # Web3 / Polygon wallet service
    └── defi.py           # DeFi operations & AI automation
```

## License

MIT License
