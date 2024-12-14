import os
from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters  # Correct import for filters

load_dotenv()

API_KEY: Final = os.getenv("API_KEY")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME")
GROUP_ID : Final = os.getenv("GROUP_ID")
CHANNEL_LINK : Final = os.getenv('CHANNEL_LINK')



async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    await update.message.reply_text(
        "እነዚህም በተሰሎንቄ ከሚኖሩት ይልቅ ልበ ሰፊዎች ነበሩና። \n"
        "ነገሩ እንደዚሁ ይሆንን? ብለው ዕለት ዕለት መጻሕፍትን እየመረመሩ ቃሉን በሙሉ ፈቃድ ተቀበሉ።\n"
        "የሐዋርያት ሥራ 17 : 11"
    )

async def message_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text
    user_name = update.effective_user.first_name
    bot_message = f"New Question from {user_name}:\n{user_question}"

    try:
        # Send the question to the targeted group
        await context.bot.send_message(chat_id=GROUP_ID, text=bot_message)
    except Exception as e:
        print(f"Failed to send message to group: {e}")

    # Thank the user
    thank_you_message = (
        "Thank you for your question! Our team will review it and provide an answer. "
        f"Please check the channel for updates: {CHANNEL_LINK}"
    )
    await update.message.reply_text(thank_you_message)




def main():
    app = ApplicationBuilder().token(API_KEY).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND , message_handle))
   

    print("Bot is running ......")
    app.run_polling(poll_interval=5,timeout=60)

if __name__ == "__main__":
    main()
