import os
import requests
import json
import time
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8132196767:AAFcTMKbjP6CEsigfR-SJ-sdxbVwH2AsxSM")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"
ADMIN_ID = "7548105589"

print("🔧 Tokio Sushi Bot ishga tushmoqda...")
user_data = {}

def send_message(chat_id, text, keyboard=None):
    try:
        url = BASE_URL + "sendMessage"
        data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
        if keyboard: data["reply_markup"] = json.dumps(keyboard)
        requests.post(url, json=data, timeout=10)
    except: pass

def main_menu():
    return {"keyboard": [["🍣 Menyu", "🛒 Savatcha"], ["📞 Aloqa", "ℹ️ Ma'lumot"]], "resize_keyboard": True}

def main():
    print("🚀 Bot ishga tushdi! Admin:", ADMIN_ID)
    last_update_id = None
    while True:
        try:
            response = requests.get(BASE_URL + "getUpdates", {"offset": last_update_id, "timeout": 30}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("ok") and data.get("result"):
                    for update in data["result"]:
                        last_update_id = update["update_id"] + 1
                        if "message" in update:
                            chat_id = update["message"]["chat"]["id"]
                            text = update["message"].get("text", "")
                            user_name = update["message"]["from"].get("first_name", "Mijoz")
                            
                            if chat_id not in user_data:
                                user_data[chat_id] = {"cart": [], "name": user_name}
                                print(f"👤 Yangi: {user_name} ({chat_id})")
                            
                            if text == "/start":
                                send_message(chat_id, "🏮 Tokio Sushi ga xush kelibsiz!", main_menu())
                            elif text == "🍣 Menyu":
                                send_message(chat_id, "🍣 Menyu tez orada!")
                            elif text == "📞 Aloqa":
                                send_message(chat_id, "📞 +998947126030")
                            else:
                                send_message(chat_id, f"Siz: {text}")
            time.sleep(1)
        except: time.sleep(3)

@app.route('/')
def home(): return "🏮 Bot ishlayapti!"

def run_bot(): main()

if __name__ == "__main__":
    bot_thread = Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
