import os
import io
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from huggingface_hub import InferenceClient

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
HF_API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")

# Model ID ကို လူသုံးများပြီး အလုပ်လုပ်နိုင်တဲ့ Model နဲ့ ပြောင်းထားပါတယ်
MODEL_ID = "stabilityai/stable-diffusion-2-1"  # ဒါမှမဟုတ် "runwayml/stable-diffusion-v1-5"

def generate_image(prompt):
    """Hugging Face InferenceClient ကိုသုံးပြီး ပုံထုတ်တယ်"""
    try:
        client = InferenceClient(model=MODEL_ID, token=HF_API_TOKEN)
        # text_to_image က PIL Image ပြန်ပေးတယ်
        image = client.text_to_image(prompt)
        # PIL Image ကို bytes အဖြစ်ပြောင်းမယ်
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes.getvalue()
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
