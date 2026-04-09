import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from services.ai_chat import chat_with_gemini, analyze_crypto_market, generate_trading_advice

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f'Hello {user.first_name}! 👋\n\n'
        f'I am your Sam AI Bot powered by Google Gemini and Polygon DeFi.\n\n'
        f'How can I help you today?\n\n'
        f'Type /help to see available commands.'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
🤖 Sam AI Bot Commands:

/start - Start the bot
/help - Show this help message
/wallet - Check your wallet
/defi - DeFi operations
/ai <message> - Chat with Gemini AI
/market - Get crypto market analysis
/advice [crypto] - Get trading advice

Just type a message and I'll respond with AI-powered insights!
    """
    await update.message.reply_text(help_text)


async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /ai command to chat with Gemini."""
    if not context.args:
        await update.message.reply_text("Please provide a message after /ai. Example: /ai What is Bitcoin?")
        return
    
    user_message = ' '.join(context.args)
    logger.info(f"User {update.effective_user.id} asked AI: {user_message}")
    
    await update.message.reply_text("🤔 Thinking...")
    response = await chat_with_gemini(user_message)
    await update.message.reply_text(response)


async def market_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /market command for crypto market analysis."""
    await update.message.reply_text("📊 Analyzing the market...")
    analysis = await analyze_crypto_market()
    await update.message.reply_text(f"📈 Market Analysis:\n\n{analysis}")


async def advice_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /advice command for trading advice."""
    crypto = ' '.join(context.args) if context.args else "Bitcoin"
    await update.message.reply_text(f"💡 Generating advice for {crypto}...")
    advice = await generate_trading_advice(crypto)
    await update.message.reply_text(f"💰 Trading Advice:\n\n{advice}")


async def wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /wallet command."""
    await update.message.reply_text(
        "💼 Wallet Features:\n\n"
        "Wallet integration coming soon!\n"
        "Connect your Polygon wallet to use DeFi features."
    )


async def defi_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /defi command."""
    await update.message.reply_text(
        "🏦 DeFi Operations:\n\n"
        "DeFi features coming soon!\n"
        "You'll be able to swap tokens, check balances, and more."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages with AI response."""
    user_message = update.message.text
    logger.info(f"User {update.effective_user.id} sent: {user_message}")
    
    response = await chat_with_gemini(user_message)
    await update.message.reply_text(response)


def create_bot_application() -> Application:
    """Create and configure the Telegram bot application."""
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")
    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('ai', ai_command))
    application.add_handler(CommandHandler('market', market_command))
    application.add_handler(CommandHandler('advice', advice_command))
    application.add_handler(CommandHandler('wallet', wallet_command))
    application.add_handler(CommandHandler('defi', defi_command))
    
    # Register message handler for non-command messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return application


def main() -> None:
    """Start the bot."""
    logger.info("Starting Telegram bot...")
    application = create_bot_application()
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Bot is running...")


if __name__ == '__main__':
    main()