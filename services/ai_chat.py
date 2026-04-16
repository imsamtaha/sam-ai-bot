import os
import time
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types

from services.metrics import record_response_time

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini API using environment variable
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Initialize client
client = None
if GOOGLE_API_KEY:
    client = genai.Client(api_key=GOOGLE_API_KEY)

# System prompt that defines the bot's persona and scope
BOT_SYSTEM_PROMPT = (
    "You are Sam, an AI-powered crypto and DeFi assistant integrated into a Telegram bot. "
    "You specialize in the Polygon blockchain ecosystem, decentralised finance (DeFi), "
    "and general cryptocurrency topics. "
    "Always be concise, friendly, and informative. "
    "Respond in plain text suitable for Telegram messages — avoid markdown headers or bullet lists "
    "that don't render well in Telegram. Use short paragraphs instead. "
    "Never provide specific financial advice or guarantee returns. "
    "When users ask about executing transactions, remind them you provide guidance only and "
    "cannot sign or broadcast transactions on their behalf. "
    "If a question is unrelated to crypto, blockchain, or DeFi, politely redirect the user to "
    "relevant topics you can help with."
)


async def chat_with_gemini(message: str) -> str:
    """Chat with Google Gemini AI and return the response."""
    try:
        if not client:
            logger.warning("GOOGLE_API_KEY not set. Please set it in your environment.")
            return "AI service is not configured. Please set the GOOGLE_API_KEY environment variable."

        start = time.monotonic()
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=BOT_SYSTEM_PROMPT,
            ),
        )
        record_response_time('gemini', time.monotonic() - start)
        return response.text
    except Exception as e:
        logger.error(f"Error chatting with Gemini: {e}")
        return "Sorry, I encountered an error processing your request. Please try again later."


async def analyze_crypto_market() -> str:
    """Analyze the crypto market using AI."""
    try:
        prompt = (
            "Give a concise overview of current cryptocurrency market conditions. "
            "Cover: the overall market sentiment (bullish/bearish/neutral), "
            "notable price movements for Bitcoin and Ethereum, "
            "any key on-chain or macro factors driving the market right now, "
            "and a brief outlook. Keep it under 250 words and avoid specific price predictions."
        )
        return await chat_with_gemini(prompt)
    except Exception as e:
        logger.error(f"Error analyzing crypto market: {e}")
        return "Error analyzing market. Please try again later."


async def generate_trading_advice(crypto: str = "Bitcoin") -> str:
    """Generate educational trading information for a specific cryptocurrency."""
    try:
        prompt = (
            f"Provide a short educational overview of {crypto} for someone interested in trading. "
            f"Cover: what {crypto} is and its use case, key factors that influence its price, "
            f"common trading strategies (e.g. DCA, swing trading, HODLing), "
            f"and the main risks to be aware of. "
            f"Keep it under 300 words. This is for educational purposes only — not financial advice."
        )
        return await chat_with_gemini(prompt)
    except Exception as e:
        logger.error(f"Error generating trading advice: {e}")
        return "Error generating advice. Please try again later."
