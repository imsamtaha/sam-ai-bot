from fastapi import FastAPI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = FastAPI()

# Initialize the Telegram bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! This is your Sam AI Bot.')

# Add command handlers
app.add_handler(CommandHandler('start', start))

@app.get("/")
async def root():
    return {'message': 'Sam AI Bot is running!'}

# Start the FastAPI server
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
