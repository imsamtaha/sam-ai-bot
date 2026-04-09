import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from services.ai_chat import chat_with_gemini, analyze_crypto_market, generate_trading_advice
from services.blockchain import get_wallet_portfolio, get_network_info, is_valid_address
from services.defi import (
    analyze_portfolio_with_ai,
    automate_blockchain_task,
    format_network_info,
    format_portfolio_message,
    get_defi_strategy,
    get_swap_info,
    list_protocols,
)

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
🤖 *Sam AI Bot Commands*

*General*
/start - Start the bot
/help - Show this help message

*AI Assistant*
/ai <message> - Chat with Gemini AI
/market - Get crypto market analysis
/advice [crypto] - Get trading advice

*Blockchain & Wallet*
/wallet <address> - View on-chain portfolio (Polygon)
/portfolio <address> - AI analysis of a wallet
/network - Polygon network status

*DeFi Automation*
/defi - List DeFi protocols on Polygon
/swap <amount> <FROM> <TO> - Swap guidance
/strategy [conservative|moderate|aggressive] - AI DeFi strategy
/automate <task> - AI-powered blockchain automation plan

Just type a message and I'll respond with AI-powered insights!
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


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
    """Handle the /wallet command — show on-chain portfolio for a Polygon address."""
    if not context.args:
        await update.message.reply_text(
            "💼 *Wallet Portfolio*\n\n"
            "Please provide a Polygon wallet address.\n"
            "Usage: `/wallet <address>`\n\n"
            "Example:\n`/wallet 0xYourPolygonAddressHere`",
            parse_mode='Markdown',
        )
        return

    address = context.args[0]
    if not is_valid_address(address):
        await update.message.reply_text(
            "❌ That doesn't look like a valid Polygon address.\n"
            "Please provide a valid 0x… address."
        )
        return

    await update.message.reply_text("🔍 Fetching wallet portfolio from Polygon…")
    portfolio = get_wallet_portfolio(address)
    await update.message.reply_text(
        format_portfolio_message(portfolio),
        parse_mode='Markdown',
    )


async def defi_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /defi command — list available DeFi protocols on Polygon."""
    protocols = list_protocols()
    lines = ["🏦 *DeFi Protocols on Polygon*\n"]
    for name, info in protocols.items():
        lines.append(
            f"*{name}* ({info['type']})\n"
            f"  {info['description']}\n"
            f"  🔗 {info['url']}\n"
        )
    lines.append(
        "Use /swap, /portfolio, /strategy, or /automate for AI-powered automation."
    )
    await update.message.reply_text('\n'.join(lines), parse_mode='Markdown')


async def swap_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /swap command — get AI guidance on swapping tokens.

    Usage: /swap <amount> <FROM_TOKEN> <TO_TOKEN>
    Example: /swap 100 USDC WMATIC
    """
    if len(context.args) < 3:
        await update.message.reply_text(
            "🔄 *Token Swap Info*\n\n"
            "Usage: `/swap <amount> <FROM> <TO>`\n\n"
            "Example: `/swap 100 USDC WMATIC`",
            parse_mode='Markdown',
        )
        return

    try:
        amount = float(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "❌ Amount must be a number. Example: `/swap 100 USDC WMATIC`",
            parse_mode='Markdown',
        )
        return

    from_token = context.args[1]
    to_token = context.args[2]

    await update.message.reply_text(
        f"🔄 Analysing swap of {amount} {from_token.upper()} → {to_token.upper()}…"
    )
    info = await get_swap_info(from_token, to_token, amount)
    await update.message.reply_text(f"🔄 *Swap Info:*\n\n{info}", parse_mode='Markdown')


async def portfolio_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /portfolio command — AI analysis of an on-chain wallet.

    Usage: /portfolio <address>
    """
    if not context.args:
        await update.message.reply_text(
            "📊 *AI Portfolio Analysis*\n\n"
            "Usage: `/portfolio <address>`\n\n"
            "Example: `/portfolio 0xYourAddressHere`",
            parse_mode='Markdown',
        )
        return

    address = context.args[0]
    await update.message.reply_text("📊 Fetching portfolio and running AI analysis…")
    analysis = await analyze_portfolio_with_ai(address)
    await update.message.reply_text(
        f"📊 *Portfolio Analysis:*\n\n{analysis}",
        parse_mode='Markdown',
    )


async def strategy_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /strategy command — AI-generated DeFi strategy.

    Usage: /strategy [conservative|moderate|aggressive]
    """
    risk = context.args[0] if context.args else "moderate"
    await update.message.reply_text(
        f"💡 Generating DeFi strategy for '{risk}' risk profile…"
    )
    strategy = await get_defi_strategy(risk)
    await update.message.reply_text(
        f"💡 *DeFi Strategy ({risk}):*\n\n{strategy}",
        parse_mode='Markdown',
    )


async def automate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /automate command — AI interprets a natural-language blockchain task.

    Usage: /automate <description of what you want to automate>
    """
    if not context.args:
        await update.message.reply_text(
            "🤖 *Blockchain Automation*\n\n"
            "Describe what you want to automate and I'll build an action plan.\n\n"
            "Usage: `/automate <task description>`\n\n"
            "Examples:\n"
            "  `/automate stake my MATIC for rewards`\n"
            "  `/automate swap USDC to WETH every week`\n"
            "  `/automate supply DAI to Aave`",
            parse_mode='Markdown',
        )
        return

    intent = ' '.join(context.args)
    await update.message.reply_text(f"🤖 Planning automation for: _{intent}_…", parse_mode='Markdown')
    plan = await automate_blockchain_task(intent)
    await update.message.reply_text(f"🤖 *Automation Plan:*\n\n{plan}", parse_mode='Markdown')


async def network_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /network command — show Polygon network status."""
    await update.message.reply_text("🌐 Fetching Polygon network info…")
    info = get_network_info()
    await update.message.reply_text(format_network_info(info), parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming text messages with AI response."""
    try:
        user_message = update.message.text
        logger.info(f"User {update.effective_user.id} sent: {user_message}")

        response = await chat_with_gemini(user_message)
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error handling message from user {update.effective_user.id}: {e}")
        await update.message.reply_text("❌ Sorry, I encountered an error. Please try again.")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming photo messages."""
    try:
        caption = update.message.caption or ""
        logger.info(f"User {update.effective_user.id} sent a photo. Caption: '{caption}'")

        if caption:
            await update.message.reply_text("🖼️ Analyzing your question...")
            response = await chat_with_gemini(
                f"A user sent a photo along with the following caption or question: '{caption}'. "
                "Please respond helpfully based on their caption. "
                "(Note: only the caption text is available, not the image itself.)"
            )
            await update.message.reply_text(response)
        else:
            await update.message.reply_text(
                "📸 I received your photo!\n\n"
                "Send it again with a caption or question and I'll do my best to help. 😊"
            )
    except Exception as e:
        logger.error(f"Error handling photo from user {update.effective_user.id}: {e}")
        await update.message.reply_text("❌ Sorry, I couldn't process your photo. Please try again.")


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming document messages."""
    doc = None
    try:
        doc = update.message.document
        caption = update.message.caption or ""
        logger.info(f"User {update.effective_user.id} sent a document: {doc.file_name}")

        if caption:
            await update.message.reply_text(
                f"📄 Received *{doc.file_name}*. Analyzing your question…",
                parse_mode='Markdown',
            )
            response = await chat_with_gemini(
                f"A user sent a document named '{doc.file_name}' with the following question or message: '{caption}'. "
                "Please respond helpfully based on their message. "
                "(Note: only the filename and caption are available, not the document content.)"
            )
            await update.message.reply_text(response)
        else:
            await update.message.reply_text(
                f"📄 I received your document: *{doc.file_name}*\n\n"
                "Send it again with a caption if you'd like me to help with something specific about it.",
                parse_mode='Markdown',
            )
    except Exception as e:
        filename = doc.file_name if doc else "unknown"
        logger.error(f"Error handling document '{filename}' from user {update.effective_user.id}: {e}")
        await update.message.reply_text("❌ Sorry, I couldn't process your document. Please try again.")


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming voice and audio messages."""
    try:
        logger.info(f"User {update.effective_user.id} sent a voice/audio message.")
        await update.message.reply_text(
            "🎙️ I received your voice message!\n\n"
            "I'm not able to transcribe audio yet — please type your message and I'll be happy to help. 😊"
        )
    except Exception as e:
        logger.error(f"Error handling voice message from user {update.effective_user.id}: {e}")
        await update.message.reply_text("❌ Sorry, I couldn't process your voice message.")


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
    application.add_handler(CommandHandler('swap', swap_command))
    application.add_handler(CommandHandler('portfolio', portfolio_command))
    application.add_handler(CommandHandler('strategy', strategy_command))
    application.add_handler(CommandHandler('automate', automate_command))
    application.add_handler(CommandHandler('network', network_command))
    
    # Register message handler for non-command text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register media handlers
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))

    return application


def main() -> None:
    """Start the bot."""
    logger.info("Starting Telegram bot...")
    application = create_bot_application()
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Bot is running...")


if __name__ == '__main__':
    main()