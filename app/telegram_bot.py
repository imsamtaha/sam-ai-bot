import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7980486380:AAHYIBG7hhIydTCE6bhkVAKl7eec9CXIKJU')

# Define a command handler for /start
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(f'Hello {user.first_name}! 👋\n\nI am your Sam AI Bot powered by Google Gemini and Polygon DeFi.\n\nHow can I help you today?')

# Define a command handler for /help
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
🤖 Sam AI Bot Commands:

/start - Start the bot
/help - Show this help message
/wallet - Check your wallet
/defi - DeFi operations
/ai - Chat with Gemini AI

Just type a message and I'll respond with AI-powered insights!
    """
    update.message.reply_text(help_text)

# Define a message handler to handle incoming messages
def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message (will be replaced with AI logic)."""
    user_message = update.message.text
    logger.info(f"User {update.effective_user.id} sent: {user_message}")
    
    # TODO: Integrate with Google Gemini AI service
    # ai_response = gemini_chat(user_message)
    
    update.message.reply_text(f"You said: {user_message}\n\n(AI response will be integrated soon)")

# Main function to start the bot
def main() -> None:
    """Start the bot."""
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    
    # Register message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    logger.info("Starting Telegram bot...")
    updater.start_polling()
    logger.info("Bot is running...")
    updater.idle()

if __name__ == '__main__':
    main()