import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ضع التوكن الجديد هنا بعد انشائه من BotFather
TOKEN = "8410258134:AAG_g-Twa_-xi45b6lnjoMz06b21PtcBTb4"

def download_video(url, folder="downloads"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    opts = {
        "outtmpl": f"{folder}/%(title)s.%(ext)s",
        "format": "mp4",
        "noplaylist": True,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        path = ydl.prepare_filename(info)
        return path

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً، أرسل رابط فيديو وسأحمله لك.")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("⏳ جاري التحميل...")

    try:
        file_path = download_video(url)
        # تحقق من حجم الملف قبل الإرسال (تليجرام يرفض الملفات الكبيرة جداً)
        if os.path.getsize(file_path) > 48 * 1024 * 1024:
            await update.message.reply_text("⚠️ الفيديو أكبر من الحد المسموح به لرفعه على تليجرام. جرب فيديو أقصر.")
        else:
            await update.message.reply_video(video=open(file_path, "rb"))
        os.remove(file_path)
    except Exception as e:
        print("❌ خطأ:", e)
        await update.message.reply_text(f"⚠️ حدث خطأ: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("🚀 البوت شغال...")
    app.run_polling()

if __name__ == "__main__":
    main()
