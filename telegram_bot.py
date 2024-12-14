import os
from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()

API_KEY: Final = os.getenv("API_KEY")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME")
GROUP_ID: Final = int(os.getenv("GROUP_ID"))  
CHANNEL_LINK: Final = os.getenv("CHANNEL_LINK")

# Debug to ensure GROUP_ID is loaded correctly
print(f"Loaded GROUP_ID: {GROUP_ID}")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    await update.message.reply_text(
        "Welcome! Send me a message, and I'll forward it to the group."
    )

async def message_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    user_chat_id = update.message.chat.id  
    user_name = update.effective_user.first_name  
    user_question = update.message.text  

  
    print(f"Message received from chat ID: {user_chat_id}")

    
    if user_chat_id == GROUP_ID:
        print("Ignoring message from the group itself.")
        return

    if update.effective_user.is_bot:
        print("Ignoring message from a bot.")
        return

   
    bot_message = f"New Question from {user_name}:\n{user_question}"

    try:
       
        await context.bot.send_message(chat_id=GROUP_ID, text=bot_message)
        print("Message forwarded to the group.")
    except Exception as e:
        print(f"Failed to send message to the group: {e}")
    
   
    thank_you_message = (
        "Thank you for your question! Our team will review it and provide an answer. "
        f"Please check the channel for updates: {CHANNEL_LINK}"
    )
    await update.message.reply_text(thank_you_message)
    print("Thank-you message sent to the user.")

def main():
    app = ApplicationBuilder().token(API_KEY).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handle))

    print("Bot is running ......")
    app.run_polling()

if __name__ == "__main__":
    main()
