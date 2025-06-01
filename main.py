import requests
import time
import telegram
import os

# Environment variables
SMS_API_URL = os.getenv("SMS_API_URL", "http://94.23.120.156/ints/sms/get-sms")
SMS_API_USER = os.getenv("SMS_API_USER")
SMS_API_PASS = os.getenv("SMS_API_PASS")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def fetch_sms():
    try:
        response = requests.post(SMS_API_URL, data={
            'username': SMS_API_USER,
            'password': SMS_API_PASS
        })
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"❌ SMS ফেচ করতে সমস্যা: {e}")
    return []

def main():
    sent_ids = set()
    while True:
        messages = fetch_sms()
        for sms in messages:
            sms_id = str(sms.get('id'))
            sender = sms.get('sender', 'Unknown')
            message = sms.get('message', '')
            if sms_id not in sent_ids:
                text = (
                    f"📥 নতুন SMS পাওয়া গেছে!\n"
                    f"👤 প্রেরক: {sender}\n"
                    f"📝 মেসেজ: {message}"
                )
                try:
                    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
                    sent_ids.add(sms_id)
                except Exception as e:
                    print(f"❌ Telegram তে পাঠাতে সমস্যা: {e}")
        time.sleep(10)

if __name__ == "__main__":
    main()