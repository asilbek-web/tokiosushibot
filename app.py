import requests
import json
import time
import os
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

app = Flask(__name__)

print("🔧 Tokio Sushi Pro Bot yuklanmoqda...")

# Bot token
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8132196767:AAFcTMKbjP6CEsigfR-SJ-sdxbVwH2AsxSM")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

# Admin ID
ADMIN_ID = "7548105589"

# Menyu ma'lumotlari
menu_data = {
    "sovuq_rollar": {
        "name": "🍣 Sovuq Rollar",
        "products": [
            {"id": 1, "name": "Filadelfiya Klassik", "price": 80000, "description": "An'anaviy filadelfiya roll"},
            {"id": 2, "name": "Filadelfiya Gold", "price": 120000, "description": "Eksklyuziv filadelfiya"},
            {"id": 3, "name": "Ebi Gold", "price": 110000, "description": "Krevetka bilan"},
            {"id": 4, "name": "Losos (gril)", "price": 93000, "description": "Grillangan losos"},
            {"id": 5, "name": "Kaliforniya s krevetkami", "price": 80000, "description": "Krevetka va avakado"},
            {"id": 6, "name": "Drakon", "price": 70000, "description": "Achchiq sous bilan"},
            {"id": 7, "name": "Kanada Gold", "price": 93000, "description": "Kanada uslubida"},
            {"id": 8, "name": "Filadelfiya Tuns", "price": 90000, "description": "Tunets bilan"},
            {"id": 9, "name": "Roll Ogrurets", "price": 65000, "description": "Bodring bilan"}
        ]
    },
    "issiq_rollar": {
        "name": "🔥 Issiq Rollar", 
        "products": [
            {"id": 10, "name": "Tempura s lososem", "price": 70000, "description": "Losos tempura"},
            {"id": 11, "name": "Tempura tuntsa", "price": 75000, "description": "Tunets tempura"},
            {"id": 12, "name": "Tempura kuritsa", "price": 48000, "description": "Tovuq tempura"},
            {"id": 13, "name": "Tempura krevetka", "price": 55000, "description": "Krevetka tempura"}
        ]
    },
    "setlar": {
        "name": "🎎 Setlar",
        "products": [
            {"id": 14, "name": "Set Tokuo", "price": 250000, "description": "Eksklyuziv to'plam"},
            {"id": 15, "name": "Set Ideal", "price": 260000, "description": "Ideal kombinatsiya"},
            {"id": 16, "name": "Set Sakura", "price": 180000, "description": "Sakura mavsumi"},
            {"id": 17, "name": "Set Klassicheskiy", "price": 150000, "description": "An'anaviy set"},
            {"id": 18, "name": "Set Okay", "price": 240000, "description": "Okay kombinatsiya"},
            {"id": 19, "name": "Set Yamomoto", "price": 250000, "description": "Yamomoto maxsus"}
        ]
    },
    "ichimliklar": {
        "name": "🥤 Ichimliklar",
        "products": [
            {"id": 20, "name": "Kok kola", "price": 19000, "description": "0.5L"},
            {"id": 21, "name": "Fanta", "price": 19000, "description": "0.5L"},
            {"id": 22, "name": "Pesti Lipton", "price": 14000, "description": "Muzli choy"},
            {"id": 23, "name": "Pivo", "price": 20000, "description": "0.5L"},
            {"id": 24, "name": "Mojito", "price": 20000, "description": "Mojito kokteyl"},
            {"id": 25, "name": "Choy Limon", "price": 25000, "description": "Limonli choy"},
            {"id": 26, "name": "Choy Toxno", "price": 35000, "description": "Maxsus choy"},
            {"id": 27, "name": "Milkshake", "price": 30000, "description": "Shokoladli milksheyk"}
        ]
    },
    "boshqa_taomlar": {
        "name": "🍱 Boshqa Taomlar",
        "products": [
            {"id": 28, "name": "Gunkun tunets", "price": 30000, "description": "Tunets gunkan"},
            {"id": 29, "name": "Gunkun losos", "price": 24000, "description": "Losos gunkan"},
            {"id": 30, "name": "Mini roll losos", "price": 24000, "description": "Kichik losos roll"},
            {"id": 31, "name": "Susi tunets", "price": 25000, "description": "Tunets sushi"},
            {"id": 32, "name": "Krab sendvich", "price": 35000, "description": "Krab sendvich"},
            {"id": 33, "name": "Slirovye sharik", "price": 22000, "description": "Sir sharik"},
            {"id": 34, "name": "Gambuger", "price": 39000, "description": "Gamburger"},
            {"id": 35, "name": "Miks pizza", "price": 95000, "description": "Aralash pizza"}
        ]
    }
}

# Foydalanuvchilar ma'lumoti
user_data = {}

def send_message(chat_id, text, keyboard=None):
    try:
        url = BASE_URL + "sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        if keyboard:
            data["reply_markup"] = json.dumps(keyboard)
        requests.post(url, json=data, timeout=10)
    except Exception as e:
        print(f"Xabar yuborishda xato: {e}")

def main_menu():
    return {
        "keyboard": [
            ["🍣 Menyu", "🛒 Savatcha"],
            ["📞 Aloqa", "ℹ️ Ma'lumot"]
        ],
        "resize_keyboard": True
    }

def categories_menu():
    keyboard = []
    for category_key, category_data in menu_data.items():
        keyboard.append([category_data["name"]])
    keyboard.append(["⬅️ Orqaga"])
    return {"keyboard": keyboard, "resize_keyboard": True}

def show_category(chat_id, category_key):
    category = menu_data[category_key]
    text = f"<b>{category['name']}</b>\n\n"
    
    for product in category["products"]:
        text += f"🍣 <b>{product['name']}</b>\n"
        text += f"💰 {product['price']:,} so'm\n"
        text += f"📝 {product['description']}\n\n"
    
    text += "Tanlang:"
    send_message(chat_id, text, main_menu())

def main():
    print("🚀 Tokio Sushi Bot ishga tushdi!")
    print(f"👑 Admin: {ADMIN_ID}")
    
    last_update_id = None
    while True:
        try:
            response = requests.get(BASE_URL + "getUpdates", {
                "offset": last_update_id,
                "timeout": 30
            }, timeout=10)
            
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
                                print(f"👤 Yangi foydalanuvchi: {user_name} ({chat_id})")
                            
                            if text == "/start":
                                welcome_text = f"""
🏮 <b>Tokio Sushi</b> ga xush kelibsiz, {user_name}!

🚚 30-45 daqiqada yetkazamiz
💵 Minimal buyurtma: 50,000 so'm
🕒 Ish vaqti: 11:00-02:00
📞 +998947126030

<b>Menyudan tanlang:</b>
                                """
                                send_message(chat_id, welcome_text, main_menu())
                            
                            elif text == "🍣 Menyu":
                                send_message(chat_id, "Kategoriya tanlang:", categories_menu())
                            
                            elif text in [category["name"] for category in menu_data.values()]:
                                for category_key, category_data in menu_data.items():
                                    if category_data["name"] == text:
                                        show_category(chat_id, category_key)
                                        break
                            
                            elif text == "📞 Aloqa":
                                contact_text = """
📞 <b>Aloqa ma'lumotlari:</b>

📍 Qarshi shahri
📱 +998901234567
🕒 11:00 - 02:00
🚚 Yetkazish: 30-45 daqiqa

💬 @tokio_sushi_support
                                """
                                send_message(chat_id, contact_text, main_menu())
                            
                            elif text == "ℹ️ Ma'lumot":
                                info_text = """
ℹ️ <b>Ma'lumot:</b>

• Yetkazib berish: 30-45 daqiqa
• Minimal buyurtma: 50,000 so'm
• To'lov: Naqd, Click, Payme
• Ish vaqti: 09:00-23:00

📞 +998947126030
                                """
                                send_message(chat_id, info_text, main_menu())
                            
                            elif text == "⬅️ Orqaga":
                                send_message(chat_id, "Bosh menyu:", main_menu())
                            
                            elif any(product["name"] in text for category in menu_data.values() for product in category["products"]):
                                send_message(chat_id, f"✅ '{text}' savatchaga qo'shildi!", main_menu())
                                admin_msg = f"🛒 Yangi buyurtma:\n👤 {user_name}\n🍣 {text}\n⏰ {datetime.now().strftime('%H:%M')}"
                                send_message(ADMIN_ID, admin_msg)
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Xato: {e}")
            time.sleep(3)

@app.route('/')
def home():
    return "🏮 Tokio Sushi Bot ishlayapti! 🍣"

@app.route('/health')
def health():
    return "OK"

def run_bot():
    main()

if __name__ == "__main__":
    bot_thread = Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
