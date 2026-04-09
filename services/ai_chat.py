import os
import logging
from dotenv import load_dotenv
from google import genai

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


async def chat_with_gemini(message: str) -> str:
    """Chat with Google Gemini AI and return the response."""
    try:
        if not client:
            logger.warning("GOOGLE_API_KEY not set. Please set it in your environment.")
            return "AI service is not configured. Please set the GOOGLE_API_KEY environment variable."
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=message
        )
        return response.text
    except Exception as e:
        logger.error(f"Error chatting with Gemini: {e}")
        return "Sorry, I encountered an error processing your request. Please try again later."


async def analyze_crypto_market() -> str:
    """Analyze the crypto market using AI."""
    try:
        prompt = """Provide a brief analysis of the current cryptocurrency market trends. 
        Include major coins like Bitcoin and Ethereum, and any significant market movements."""
        return await chat_with_gemini(prompt)
    except Exception as e:
        logger.error(f"Error analyzing crypto market: {e}")
        return "Error analyzing market. Please try again later."


async def generate_trading_advice(crypto: str = "Bitcoin") -> str:
    """Generate trading advice for a specific cryptocurrency."""
    try:
        prompt = f"""Provide general educational information about {crypto} trading strategies. 
        Note: This is for educational purposes only and not financial advice."""
        return await chat_with_gemini(prompt)
    except Exception as e:
        logger.error(f"Error generating trading advice: {e}")
        return "Error generating advice. Please try again later."
