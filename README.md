# 🤖 Telegram News Bot

این ربات اخبار را از فید خبری zoomit دریافت کرده، ترجمه و خلاصه کرده و به کانال تلگرام ارسال می‌کند.

## 💡 ویژگی‌ها
- دریافت خودکار اخبار از RSS
- ترجمه به فارسی با Google Translate
- خلاصه‌سازی با Google Gemini
- ارسال خبر + تصویر به کانال تلگرام
- اجرا هر ۲ ساعت به صورت خودکار

## ⚙️ متغیرهای محیطی مورد نیاز
در محیط اجرا (مثلاً Render.com) موارد زیر را به عنوان Environment Variable تنظیم کن:

- BOT_TOKEN → توکن ربات تلگرام
- CHANNEL_ID → آیدی کانال (با -100 شروع می‌شود)
- GOOGLE_API_KEY → کلید API مربوط به Google Gemini

## 🧪 اجرای محلی

```bash
pip install -r requirements.txt
python bot.py
