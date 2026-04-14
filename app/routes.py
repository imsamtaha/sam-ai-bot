import logging
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from telegram import Update

from services.ai_chat import chat_with_gemini, analyze_crypto_market, generate_trading_advice
from services.blockchain import get_wallet_portfolio, get_network_info, is_valid_address
from services.defi import (
    analyze_portfolio_with_ai,
    automate_blockchain_task,
    get_defi_strategy,
    get_swap_info,
    list_protocols,
)

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
    crypto: Optional[str] = Field(default="Bitcoin")


class SwapRequest(BaseModel):
    """Request model for swap information."""
    from_token: str
    to_token: str
    amount: float = Field(gt=0)


class PortfolioRequest(BaseModel):
    """Request model for portfolio analysis."""
    address: str


class StrategyRequest(BaseModel):
    """Request model for DeFi strategy."""
    risk_profile: Optional[str] = Field(default="moderate")


class AutomateRequest(BaseModel):
    """Request model for blockchain automation."""
    intent: str


# Telegram webhook endpoint
@router.post('/webhook')
async def telegram_webhook(request: Request):
    """Handle incoming Telegram webhook updates."""
    telegram_application = getattr(request.app.state, 'telegram_application', None)
    if telegram_application is None:
        raise HTTPException(status_code=503, detail="Telegram bot is not initialized")

    try:
        data = await request.json()
        update = Update.de_json(data, telegram_application.bot)
        if update is not None:
            await telegram_application.process_update(update)
        return JSONResponse({'status': 'received', 'ok': True})
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


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
        raise HTTPException(status_code=500, detail="Failed to process AI request")


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
        raise HTTPException(status_code=500, detail="Failed to analyze market")


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
        raise HTTPException(status_code=500, detail="Failed to generate advice")


# ---------------------------------------------------------------------------
# Blockchain / DeFi endpoints
# ---------------------------------------------------------------------------

@router.get('/blockchain/network')
async def blockchain_network_endpoint():
    """Get Polygon network status."""
    try:
        info = get_network_info()
        return JSONResponse({'status': 'success', 'network': info})
    except Exception as e:
        logger.error(f"Error fetching network info: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch network info")


@router.get('/blockchain/wallet/{address}')
async def blockchain_wallet_endpoint(address: str):
    """Get on-chain portfolio for a Polygon wallet address."""
    if not is_valid_address(address):
        raise HTTPException(status_code=400, detail=f"Invalid address: {address}")
    try:
        portfolio = get_wallet_portfolio(address)
        return JSONResponse({'status': 'success', 'portfolio': portfolio})
    except Exception as e:
        logger.error(f"Error fetching wallet portfolio: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch wallet portfolio")


@router.post('/blockchain/portfolio/analyze')
async def blockchain_portfolio_analyze_endpoint(request: PortfolioRequest):
    """AI analysis of a Polygon wallet portfolio."""
    if not is_valid_address(request.address):
        raise HTTPException(status_code=400, detail=f"Invalid address: {request.address}")
    try:
        analysis = await analyze_portfolio_with_ai(request.address)
        return JSONResponse({'status': 'success', 'analysis': analysis})
    except Exception as e:
        logger.error(f"Error analysing portfolio: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyse portfolio")


@router.get('/defi/protocols')
async def defi_protocols_endpoint():
    """List available DeFi protocols on Polygon."""
    try:
        protocols = list_protocols()
        return JSONResponse({'status': 'success', 'protocols': protocols})
    except Exception as e:
        logger.error(f"Error listing DeFi protocols: {e}")
        raise HTTPException(status_code=500, detail="Failed to list protocols")


@router.post('/defi/swap')
async def defi_swap_endpoint(request: SwapRequest):
    """Get AI guidance on a token swap on Polygon."""
    try:
        info = await get_swap_info(request.from_token, request.to_token, request.amount)
        return JSONResponse({
            'status': 'success',
            'swap_info': info,
            'from_token': request.from_token,
            'to_token': request.to_token,
            'amount': request.amount,
        })
    except Exception as e:
        logger.error(f"Error getting swap info: {e}")
        raise HTTPException(status_code=500, detail="Failed to get swap info")


@router.post('/defi/strategy')
async def defi_strategy_endpoint(request: StrategyRequest):
    """Get an AI-generated DeFi strategy for a risk profile."""
    try:
        strategy = await get_defi_strategy(request.risk_profile)
        return JSONResponse({
            'status': 'success',
            'strategy': strategy,
            'risk_profile': request.risk_profile,
        })
    except Exception as e:
        logger.error(f"Error generating DeFi strategy: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate strategy")


@router.post('/defi/automate')
async def defi_automate_endpoint(request: AutomateRequest):
    """AI-powered blockchain automation plan from a natural-language intent."""
    try:
        plan = await automate_blockchain_task(request.intent)
        return JSONResponse({
            'status': 'success',
            'plan': plan,
            'intent': request.intent,
        })
    except Exception as e:
        logger.error(f"Error generating automation plan: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate automation plan")
