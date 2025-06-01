import requests
import time

# Configuration
SMS_API_URL = "http://109.236.84.81/api/sms"
SMS_API_TOKEN = "g4eFcoWUgHo8T1VDQQ=="
TELEGRAM_BOT_TOKEN = "7612118596:AAFzuo-2q_i8oxxrd6C6a8pmx4JCBJAlwRs"
TELEGRAM_CHAT_ID = "-1002535103722"

last_sms_id = None

def get_sms():
    try:
        response = requests.get(
            SMS_API_URL,
            headers={"Authorization": f"Bearer {SMS_API_TOKEN}"},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("messages", [])
    except Exception as e:
        print("Failed to fetch SMS:", e)
        return []

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram send failed:", e)

def main_loop():
    global last_sms_id
    while True:
        messages = get_sms()
        if messages:
            for msg in messages:
                msg_id = msg.get("id")
                if msg_id != last_sms_id:
                    sms_text = msg.get("text", "📩 New SMS Received")
                    send_to_telegram(f"📨 <b>SMS:</b>
{sms_text}")
                    last_sms_id = msg_id
        time.sleep(10)

if __name__ == "__main__":
    print("✅ Bot is running...")
    main_loop()
    
