import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")

app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "Bot is running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 Musiqa nomini yozing!")

async def search_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"🔍 '{query}' qidirilmoqda...")
    ydl_opts = {'format': 'bestaudio/best','noplaylist': True,'quiet': True,'outtmpl': '%(title)s.%(ext)s','postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            if 'entries' in info: info = info['entries'][0]
            mp3 = ydl.prepare_filename(info).rsplit('.',1)[0] + ".mp3"
            with open(mp3, 'rb') as audio:
                await update.message.reply_audio(audio=audio, title=info.get('title', query))
            os.remove(mp3)
    except Exception as e:
        await update.message.reply_text(f"Xato: {e}")

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_music))
    app.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)
