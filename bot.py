import os
import feedparser
import time
import requests
from bs4 import BeautifulSoup
import schedule
from googletrans import Translator
import google.generativeai as genai
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = Bot(token=BOT_TOKEN)
translator = Translator()

sent_articles = set()

def fetch_articles():
    feed_url = "https://www.zoomit.ir/feed/"
    feed = feedparser.parse(feed_url)
    return feed.entries

def get_article_image(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        img_tag = soup.find('img')
        if img_tag and 'src' in img_tag.attrs:
            return img_tag['src']
    except Exception as e:
        print("❌ خطا در دریافت عکس:", e)
    return None

def summarize_with_gemini(text):
    try:
        response = model.generate_content(f"خلاصه‌ای فارسی، کوتاه و مفید از متن زیر بنویس:\n{text}")
        return response.text.strip()
    except Exception as e:
        print("❌ خطا در خلاصه‌سازی:", e)
        return None

def translate_to_farsi(text):
    try:
        return translator.translate(text, dest='fa').text
    except Exception as e:
        print("❌ خطا در ترجمه:", e)
        return text

def send_to_telegram(title, link, summary, image_url):
    caption = f"📰 {title}\n\n📝 {summary}\n\n🔗 {link}"
    try:
        if image_url:
            bot.send_photo(chat_id=CHANNEL_ID, photo=image_url, caption=caption[:1024])
        else:
            bot.send_message(chat_id=CHANNEL_ID, text=caption)
    except Exception as e:
        print("❌ خطا در ارسال:", e)

def run_bot():
    print("✅ اجرای run_bot آغاز شد")
    articles = fetch_articles()
    print(f"🔎 تعداد خبرها: {len(articles)}")

    for article in articles:
        if article.link not in sent_articles:
            print(f"📌 خبر جدید: {article.title}")
            sent_articles.add(article.link)

            content = article.get("summary", "") or article.get("description", "")
            translated = translate_to_farsi(content)
            print("📝 ترجمه انجام شد")

            summary = summarize_with_gemini(translated)
            print("✍ خلاصه‌سازی انجام شد")

            image_url = get_article_image(article.link)
            print(f"🖼 آدرس عکس: {image_url}")

            send_to_telegram(article["title"], article["link"], summary, image_url)
            print("📤 پیام ارسال شد")
            time.sleep(2)

schedule.every(2).hours.do(run_bot)

run_bot()

while True:
    schedule.run_pending()
    time.sleep(10)
