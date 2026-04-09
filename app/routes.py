import logging
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

from services.ai_chat import chat_with_gemini, analyze_crypto_market, generate_trading_advice

# Set up logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


class AIRequest(BaseModel):
    """Request model for AI endpoints."""
    message: str
    context: Optional[str] = None


class MarketRequest(BaseModel):
    """Request model for market analysis."""
    crypto: Optional[str] = "Bitcoin"


# Telegram webhook endpoint
@router.post('/webhook')
async def telegram_webhook(request: Request):
    """Handle incoming Telegram webhook updates."""
    try:
        data = await request.json()
        logger.info(f"Received webhook data: {data}")
        # Process the incoming Telegram update here
        # This will be integrated with the bot application
        return JSONResponse({'status': 'received', 'ok': True})
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/ai/chat')
async def ai_chat_endpoint(request: AIRequest):
    """Chat with AI endpoint."""
    try:
        response = await chat_with_gemini(request.message)
        return JSONResponse({
            'status': 'success',
            'response': response
        })
    except Exception as e:
        logger.error(f"Error in AI chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/ai/market')
async def ai_market_endpoint():
    """Get AI market analysis."""
    try:
        analysis = await analyze_crypto_market()
        return JSONResponse({
            'status': 'success',
            'analysis': analysis
        })
    except Exception as e:
        logger.error(f"Error in market analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/ai/advice')
async def ai_advice_endpoint(request: MarketRequest):
    """Get AI trading advice."""
    try:
        advice = await generate_trading_advice(request.crypto)
        return JSONResponse({
            'status': 'success',
            'advice': advice,
            'crypto': request.crypto
        })
    except Exception as e:
        logger.error(f"Error generating advice: {e}")
        raise HTTPException(status_code=500, detail=str(e))
