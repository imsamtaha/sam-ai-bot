import os
import asyncio
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

from app.routes import router
from app.telegram_bot import create_bot_application

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    logger.info("Starting Sam AI Bot application...")

    use_webhook = os.getenv('USE_WEBHOOK', 'false').lower() == 'true'
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')

    if use_webhook and telegram_token:
        bot_app = create_bot_application()
        await bot_app.initialize()
        await bot_app.start()
        app.state.bot_app = bot_app
        logger.info("Telegram bot application initialised for webhook mode")

        webhook_url = os.getenv('WEBHOOK_URL', '').rstrip('/')
        if webhook_url:
            if not webhook_url.startswith('https://'):
                logger.warning(
                    f"WEBHOOK_URL '{webhook_url}' does not start with 'https://' — "
                    "Telegram requires a valid HTTPS URL. Webhook registration skipped."
                )
            else:
                await bot_app.bot.set_webhook(url=f"{webhook_url}/webhook")
                logger.info(f"Telegram webhook registered at {webhook_url}/webhook")
        else:
            logger.warning(
                "WEBHOOK_URL is not set — Telegram will not forward updates to this server. "
                "Set WEBHOOK_URL to the public base URL of this application."
            )

    yield

    if use_webhook and hasattr(app.state, 'bot_app'):
        await app.state.bot_app.stop()
        await app.state.bot_app.shutdown()

    logger.info("Shutting down Sam AI Bot application...")


# Create FastAPI app
app = FastAPI(
    title="Sam AI Bot",
    description="AI-powered Telegram bot with Google Gemini and Polygon DeFi integration",
    version="1.0.0",
    lifespan=lifespan
)

# Include routes
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        'status': 'running',
        'message': 'Sam AI Bot is running!',
        'version': '1.0.0'
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {'status': 'healthy'}


if __name__ == '__main__':
    import uvicorn
    
    # Check if running in webhook mode or polling mode
    use_webhook = os.getenv('USE_WEBHOOK', 'false').lower() == 'true'
    
    if use_webhook:
        # Run FastAPI server for webhook mode
        port = int(os.getenv('PORT', 8000))
        logger.info(f"Starting FastAPI server on port {port} (webhook mode)...")
        uvicorn.run(app, host='0.0.0.0', port=port)
    else:
        # Run Telegram bot in polling mode
        logger.info("Starting Telegram bot in polling mode...")
        bot_app = create_bot_application()
        bot_app.run_polling()
