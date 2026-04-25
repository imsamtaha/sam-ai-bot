import os
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
    telegram_application = None

    if use_webhook:
        webhook_secret = os.getenv('TELEGRAM_WEBHOOK_SECRET', '').strip()
        if not webhook_secret:
            raise ValueError(
                "TELEGRAM_WEBHOOK_SECRET environment variable must be set when USE_WEBHOOK=true"
            )

        telegram_application = create_bot_application()
        await telegram_application.initialize()
        await telegram_application.start()

        webhook_base_url = os.getenv('TELEGRAM_WEBHOOK_URL', '').strip()
        if webhook_base_url:
            webhook_url = f"{webhook_base_url.rstrip('/')}/webhook"
            await telegram_application.bot.set_webhook(
                url=webhook_url,
                secret_token=webhook_secret,
            )
            logger.info(f"Telegram webhook configured: {webhook_url}")
        else:
            logger.warning(
                "TELEGRAM_WEBHOOK_URL is not set. "
                "Configure the Telegram webhook URL manually."
            )

        app.state.telegram_application = telegram_application
        app.state.telegram_webhook_secret = webhook_secret

    yield

    if telegram_application is not None:
        await telegram_application.stop()
        await telegram_application.shutdown()

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
