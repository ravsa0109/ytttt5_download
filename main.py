from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import yt_dlp
import os
import uuid

BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"  # ← Replace with your token

def start(update, context):
    update.message.reply_text("👋 Send me a YouTube link. I’ll download it in 360p.")

def download_video(update, context):
    url = update.message.text
    if "youtube.com" not in url and "youtu.be" not in url:
        update.message.reply_text("❌ Please send a valid YouTube link.")
        return

    update.message.reply_text("⏬ Downloading your video, please wait...")

    try:
        filename = f"{uuid.uuid4()}.mp4"
        ydl_opts = {
            'format': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
            'outtmpl': filename,
            'merge_output_format': 'mp4',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        update.message.reply_video(video=open(filename, 'rb'))
        os.remove(filename)

    except Exception as e:
        update.message.reply_text(f"⚠️ Error: {e}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
