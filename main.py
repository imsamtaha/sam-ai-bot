import os
import time
import asyncio
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Request

from app.routes import router
from app.telegram_bot import create_bot_application
from services.metrics import record_request, record_error, record_response_time

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
    yield
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


@app.middleware('http')
async def metrics_middleware(request: Request, call_next):
    """Track request counts and response times for all HTTP endpoints."""
    endpoint = request.url.path
    record_request(endpoint)
    start = time.monotonic()
    try:
        response = await call_next(request)
        if response.status_code >= 500:
            record_error(endpoint)
        return response
    except Exception:
        record_error(endpoint)
        raise
    finally:
        record_response_time(endpoint, time.monotonic() - start)


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
