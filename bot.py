import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Environment Variables ကနေ Token တွေယူပါ
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
HF_API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")

def generate_image(prompt):
    """Hugging Face API ကိုသုံးပြီး ပုံထုတ်တယ်"""
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=60)
        if response.status_code == 200:
            return response.content
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **AI Image Generator Bot**\n\n"
        "ပုံထုတ်ချင်တဲ့ စာသား (Prompt) ကိုပို့ပါ။\n\n"
        "**ဥပမာ:**\n"
        "- `လှပတဲ့ အမျိုးသမီး၊ လက်တွေ့ဆန်ဆန်`\n"
        "- `anime မိန်းကလေး၊ ဆံပင်ရှည်`"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await update.message.reply_text("⏳ ပုံထုတ်နေပါပြီ... စက္ကန့် ၃၀ ခန့်စောင့်ပါ")
    
    image_data = generate_image(prompt)
    
    if image_data:
        await update.message.reply_photo(
            photo=image_data,
            caption=f"✅ အောင်မြင်ပါပြီ! Prompt: {prompt[:100]}"
        )
    else:
        await update.message.reply_text("❌ ပုံထုတ်မအောင်မြင်ပါ။ နောက်တစ်ခါ ထပ်စမ်းပါ။")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Bot အလုပ်လုပ်နေပါပြီ...")
    app.run_polling()

if __name__ == "__main__":
    main()
