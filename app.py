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
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
        if keyboard:
            data["reply_markup"] = json.dumps(keyboard)
        requests.post(url, json=data, timeout=10)
    except Exception as e:
        print(f"Xabar yuborishda xato: {e}")

def request_contact(chat_id):
    keyboard = {
        "keyboard": [[{"text": "📞 Telefon raqamni yuborish", "request_contact": True}]],
        "resize_keyboard": True
    }
    send_message(chat_id, "📞 <b>Telefon raqamingizni yuboring:</b>\n\nPastdagi tugmani bosing yoki +998... formatida yozing:", keyboard)

def request_location(chat_id):
    keyboard = {
        "keyboard": [[{"text": "📍 Lokatsiyani yuborish", "request_location": True}]],
        "resize_keyboard": True
    }
    send_message(chat_id, "📍 <b>Lokatsiyangizni yuboring:</b>\n\nPastdagi tugmani bosing yoki manzil yozing:", keyboard)

def main_menu():
    return {
        "keyboard": [
            ["🍣 Menyu", "🛒 Savatcha"],
            ["📞 Aloqa", "⭐ Bizni baholash"],
            ["📢 Aksiyalar", "ℹ️ Ma'lumot"]
        ],
        "resize_keyboard": True
    }

def categories_menu():
    keyboard = []
    row = []
    for category_key, category_data in menu_data.items():
        row.append(category_data["name"])
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append(["🛒 Savatcha", "⬅️ Orqaga"])
    return {"keyboard": keyboard, "resize_keyboard": True}

def products_menu(category_key):
    products = menu_data[category_key]["products"]
    keyboard = []
    for product in products:
        btn_text = f"{product['name']} - {product['price']:,} so'm"
        keyboard.append([btn_text])
    
    keyboard.append(["🛒 Savatcha", "📥 Boshqa kategoriya"])
    keyboard.append(["⬅️ Bosh menyu"])
    return {"keyboard": keyboard, "resize_keyboard": True}

def cart_menu():
    return {
        "keyboard": [
            ["✅ Buyurtma berish", "🔄 Savatchani tozalash"],
            ["✏️ Mahsulot o'zgartirish", "📥 Menyuga qaytish"],
            ["⬅️ Bosh menyu"]
        ],
        "resize_keyboard": True
    }

def show_category(chat_id, category_key):
    category = menu_data[category_key]
    text = f"<b>{category['name']}</b>\n\n"
    
    for product in category["products"]:
        text += f"🍣 <b>{product['name']}</b>\n"
        text += f"💰 {product['price']:,} so'm\n"
        text += f"📝 {product['description']}\n\n"
    
    text += "🛒 <b>Mahsulot tanlash uchun pastdagi tugmalardan birini bosing!</b>"
    send_message(chat_id, text, products_menu(category_key))

def add_to_cart(chat_id, product_name):
    product = None
    for category in menu_data.values():
        for p in category["products"]:
            if p["name"] in product_name:
                product = p
                break
        if product:
            break
    
    if product:
        if chat_id not in user_data:
            user_data[chat_id] = {"cart": [], "name": "Mijoz"}
        
        user_data[chat_id]["cart"].append(product)
        
        cart_count = len(user_data[chat_id]["cart"])
        send_message(chat_id, f"✅ <b>{product['name']}</b> savatchaga qo'shildi!\n\n🛒 Savatchada: {cart_count} ta mahsulot", main_menu())
        
        user_name = user_data[chat_id]["name"]
        admin_msg = f"🛒 <b>Yangi mahsulot qo'shildi:</b>\n👤 {user_name} (ID: {chat_id})\n🍣 {product['name']}\n💰 {product['price']:,} so'm\n⏰ {datetime.now().strftime('%H:%M')}"
        send_message(ADMIN_ID, admin_msg)
    else:
        send_message(chat_id, "❌ Mahsulot topilmadi. Iltimos, qaytadan urinib ko'ring.")

def show_cart(chat_id):
    if chat_id not in user_data or "cart" not in user_data[chat_id] or not user_data[chat_id]["cart"]:
        send_message(chat_id, "🛒 <b>Savatchangiz bo'sh</b>\n\nMenyudan mahsulot tanlang!", main_menu())
        return
    
    cart = user_data[chat_id]["cart"]
    text = "<b>🛒 Sizning savatchangiz</b>\n\n"
    total = 0
    
    for i, product in enumerate(cart, 1):
        text += f"{i}. {product['name']} - {product['price']:,} so'm\n"
        total += product["price"]
    
    text += f"\n<b>💰 Jami: {total:,} so'm</b>"
    text += f"\n\n⏰ Yetkazish vaqti: <b>30-45 daqiqa</b>"
    text += f"\n🚚 Yetkazib berish: <b>TEKIN</b>"
    
    send_message(chat_id, text, cart_menu())

def start_order(chat_id):
    if chat_id not in user_data or "cart" not in user_data[chat_id] or not user_data[chat_id]["cart"]:
        send_message(chat_id, "❌ Savatchangiz bo'sh. Avval mahsulot tanlang!", main_menu())
        return
    
    user_data[chat_id]["order_stage"] = "waiting_contact"
    request_contact(chat_id)

def process_order(chat_id, contact, location):
    if chat_id not in user_data or "cart" not in user_data[chat_id]:
        return
    
    cart = user_data[chat_id]["cart"]
    total = sum(product["price"] for product in cart)
    order_id = int(time.time())
    user_name = user_data[chat_id].get("name", "Mijoz")
    
    # Google Maps havolasini yaratish
    if isinstance(location, dict) and 'latitude' in location:
        lat = location['latitude']
        lon = location['longitude']
        map_url = f"https://www.google.com/maps?q={lat},{lon}"
        location_text = f"📍 <a href='{map_url}'>Google Maps da ko'rish</a>"
        location_for_admin = f"🌐 <a href='{map_url}'>Google Maps</a> (Lat: {lat}, Lon: {lon})"
    else:
        location_text = location
        location_for_admin = location
    
    # Mijozga xabar
    order_text = f"""
🎉 <b>BUYURTMA QABUL QILINDI!</b>

🆔 Buyurtma raqami: <b>#{order_id}</b>
👤 Ism: <b>{user_name}</b>
📞 Telefon: <b>{contact}</b>
📍 Manzil: <b>{location_text}</b>
⏰ Yetkazish: <b>30-45 daqiqa</b>
🕒 Buyurtma vaqti: <b>{datetime.now().strftime('%H:%M')}</b>

<b>Buyurtma tafsilotlari:</b>
"""
    
    for product in cart:
        order_text += f"• {product['name']} - {product['price']:,} so'm\n"
    
    order_text += f"\n<b>💰 JAMI: {total:,} so'm</b>"
    order_text += f"\n\n📞 <b>Aloqa: +998947126030</b>"
    order_text += f"\n⏳ <b>Buyurtma tayyor bo'lishi: {((datetime.now() + timedelta(minutes=40)).strftime('%H:%M'))}</b>"
    
    send_message(chat_id, order_text, main_menu())
    
    # Adminga to'liq xabar
    admin_text = f"""
🚨 <b>YANGI BUYURTMA!</b>

🆔 #{order_id}
👤 {user_name} (ID: {chat_id})
📞 {contact}
📍 {location_for_admin}
🕒 {datetime.now().strftime('%H:%M:%S')}
💰 {total:,} so'm

<b>Mahsulotlar:</b>
"""
    
    for product in cart:
        admin_text += f"• {product['name']} - {product['price']:,} so'm\n"
    
    admin_text += f"\n⏳ Tayyor bo'lishi: {(datetime.now() + timedelta(minutes=40)).strftime('%H:%M')}"
    
    send_message(ADMIN_ID, admin_text)
    
    # Alohida Google Maps havolasi
    if isinstance(location, dict) and 'latitude' in location:
        map_message = f"""
🗺️ <b>MIJOZ LOKATSIYASI:</b>

🌐 <a href='https://www.google.com/maps?q={location['latitude']},{location['longitude']}'>Google Maps da ochish</a>
📍 Kordinatalar: {location['latitude']}, {location['longitude']}
👤 Mijoz: {user_name}
📞 Telefon: {contact}
        """
        send_message(ADMIN_ID, map_message)
    
    # Savatchani tozalash
    user_data[chat_id]["cart"] = []
    user_data[chat_id]["order_stage"] = None

def show_contact(chat_id):
    contact_text = """
📞 <b>Aloqa ma'lumotlari</b>

🏮 <b>Tokio Sushi</b>
📍 Qarshi shahar
📱 +998947126030
🕒 11:00 - 02:00
🚚 Yetkazish: 30-45 daqiqa

<b>Ijtimoiy tarmoqlar:</b>
📸 Instagram: @tokio_sushi_bar_karshi
📱 Telegram: @tokio_sushi_support

<b>Qo'llab-quvvatlash:</b>
📞 +998947126030 (24/7)
    """
    send_message(chat_id, contact_text, main_menu())

def show_info(chat_id):
    info_text = """
ℹ️ <b>Tokio Sushi haqida</b>

🌟 <b>Bizning afzalliklarimiz:</b>
• 🚚 30-45 daqiqada yetkazamiz
• 💰 Minimal buyurtma: 50,000 so'm
• 🕒 11:00-02:00 ishlaymiz
• 🌱 Yangi ingredientlar
• 👨‍🍳 Professional oshpazlar

💳 <b>To'lov usullari:</b>
• Naqd pul
• Click
• Payme
• Bank kartasi

📞 <b>Qo'llab-quvvatlash:</b>
+998947126030
    """
    send_message(chat_id, info_text, main_menu())

def show_actions(chat_id):
    actions_text = """
📢 <b>Aksiyalar va chegirmalar</b>

🎉 <b>Hozirgi aksiyalar:</b>
• 💰 10% chegirma - 100,000 so'mdan ortiq buyurtmalar
• 🎁 Bepich ichimlik - 150,000 so'mdan ortiq buyurtmalar
• 👥 Do'stingizni taklif qiling - 15% chegirma

🏆 <b>Bonus tizimi:</b>
• Har 50,000 so'm - 1 ball
• 10 ball - 10% chegirma
• 20 ball - bepul desert
    """
    send_message(chat_id, actions_text, main_menu())

def main():
    print("🚀 Tokio Sushi Pro Bot ishga tushdi!")
    print(f"👑 Admin: {ADMIN_ID}")
    print("📞 Support: +998947126030")
    print("⏰ Yetkazish: 30-45 daqiqa")
    
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
                            message_data = update["message"]
                            
                            # Kontakt qabul qilish
                            if "contact" in message_data:
                                if chat_id in user_data and user_data[chat_id].get("order_stage") == "waiting_contact":
                                    phone = message_data["contact"].get("phone_number", "")
                                    user_data[chat_id]["contact"] = phone
                                    user_data[chat_id]["order_stage"] = "waiting_location"
                                    request_location(chat_id)
                                continue
                            
                            # Lokatsiya qabul qilish - TO'G'RILANDI
                            if "location" in message_data:
                                if chat_id in user_data and user_data[chat_id].get("order_stage") == "waiting_location":
                                    location = message_data["location"]
                                    # To'g'ridan-to'g'ri location obyektini yuboramiz
                                    process_order(chat_id, user_data[chat_id]["contact"], location)
                                    user_data[chat_id]["order_stage"] = None
                                continue
                            
                            text = message_data.get("text", "")
                            user_name = message_data["from"].get("first_name", "Mijoz")
                            
                            if chat_id not in user_data:
                                user_data[chat_id] = {"cart": [], "name": user_name}
                                print(f"👤 Yangi foydalanuvchi: {user_name} ({chat_id})")
                            
                            if text == "/start":
                                welcome_text = f"""
🏮 <b>Tokio Sushi</b> ga xush kelibsiz, {user_name}! 🎌

• 🚚 30-45 daqiqada yetkazamiz
• 💰 Minimal buyurtma: 50,000 so'm  
• 🕒 Ish vaqti: 11:00-02:00
• 🌟 Sifat kafolati

<b>Quyidagi menyudan tanlang:</b>
                                """
                                send_message(chat_id, welcome_text, main_menu())
                            
                            elif text == "🍣 Menyu":
                                send_message(chat_id, "🍣 <b>Kategoriyalar:</b>", categories_menu())
                            
                            elif text == "🛒 Savatcha":
                                show_cart(chat_id)
                            
                            elif text == "✅ Buyurtma berish":
                                start_order(chat_id)
                            
                            elif text == "🔄 Savatchani tozalash":
                                if chat_id in user_data:
                                    user_data[chat_id]["cart"] = []
                                send_message(chat_id, "✅ Savatcha tozalandi!", main_menu())
                            
                            elif text == "📞 Aloqa":
                                show_contact(chat_id)
                            
                            elif text == "ℹ️ Ma'lumot":
                                show_info(chat_id)
                            
                            elif text == "📢 Aksiyalar":
                                show_actions(chat_id)
                            
                            elif text in ["⬅️ Orqaga", "⬅️ Bosh menyu", "📥 Menyuga qaytish"]:
                                send_message(chat_id, "🏠 Bosh menyu", main_menu())
                            
                            elif text == "📥 Boshqa kategoriya":
                                send_message(chat_id, "🍣 <b>Kategoriyalar:</b>", categories_menu())
                            
                            elif any(category_data["name"] == text for category_data in menu_data.values()):
                                for category_key, category_data in menu_data.items():
                                    if category_data["name"] == text:
                                        show_category(chat_id, category_key)
                                        break
                            
                            elif any(product["name"] in text for category in menu_data.values() for product in category["products"]):
                                add_to_cart(chat_id, text)
                            
                            elif text.startswith("+998") and len(text) == 13:
                                if chat_id in user_data and user_data[chat_id].get("order_stage") == "waiting_contact":
                                    user_data[chat_id]["contact"] = text
                                    user_data[chat_id]["order_stage"] = "waiting_location"
                                    request_location(chat_id)
                            
                            elif text and text != "/start":
                                send_message(chat_id, "❌ Noma'lum buyruq. Iltimos, menyudan foydalaning.", main_menu())
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Xato: {e}")
            time.sleep(3)

@app.route('/')
def home():
    return "🏮 Tokio Sushi Pro Bot ishlayapti! 🍣"

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
