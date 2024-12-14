import os
import telebot
from typing import final
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

API_KEY : final =  os.getenv('API_KEY')
BOT_USERNAME : final = os.getenv('BOT_USERNAME')

async def start_command(update : Update, context : ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('')