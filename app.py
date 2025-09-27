import requests
import json
import time
import os
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread
import schedule

app = Flask(__name__)

print("🎌 TOKIO SUSHI PREMIUM BOT yuklanmoqda...")

# Sozlamalar
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8132196767:AAFcTMKbjP6CEsigfR-SJ-sdxbVwH2AsxSM")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"
ADMIN_ID = "7548105589"
DELIVERY_PRICE = 15000
WORK_HOURS = "11:00 - 02:00"
PREPARATION_TIME = "30-45 daqiqa"

# Premium menyu ma'lumotlari
menu_data = {
    "issiq_taomlar": {
        "name": "🍜 Issiq Taomlar",
        "emoji": "🍜",
        "products": [
            {"id": 1, "name": "Рамэн Классик", "price": 80000, "description": "An'anaviy yapon rameni", "prep_time": "20 daqiqa"},
            {"id": 2, "name": "Рамэн Токио", "price": 66000, "description": "Maxsus ramen", "prep_time": "25 daqiqa"},
            {"id": 3, "name": "Вок с говядиной", "price": 65000, "description": "Mol go'shti bilan vok", "prep_time": "15 daqiqa"},
            {"id": 4, "name": "Том Ям Токио", "price": 95000, "description": "Taylandcha Tom Yam", "prep_time": "30 daqiqa"},
            {"id": 5, "name": "Куриные крылышки", "price": 35000, "description": "Qovurilgan tovuq qanotchalar", "prep_time": "15 daqiqa"}
        ]
    },
    "sovuq_rollar": {
        "name": "🍣 Premium Rollar",
        "emoji": "🍣",
        "products": [
            {"id": 6, "name": "Филадельфия Голд", "price": 120000, "description": "Сыр.Лосось.Огурец.Угорь", "prep_time": "15 daqiqa"},
            {"id": 7, "name": "Филадельфия Классик", "price": 80000, "description": "Сыр.Огурецы.Лосось", "prep_time": "12 daqiqa"},
            {"id": 8, "name": "Калифорния с креветками", "price": 80000, "description": "Сыр.Огурец.Креветки", "prep_time": "12 daqiqa"}
        ]
    },
    "pishirilgan_rollar": {
        "name": "🔥 Pishirilgan Rollar",
        "emoji": "🔥",
        "products": [
            {"id": 9, "name": "Ролл с креветкой", "price": 80000, "description": "Сыр.Тигровые креветки", "prep_time": "18 daqiqa"},
            {"id": 10, "name": "Ролл с угрем", "price": 80000, "description": "Сыр.огурецы.угорь", "prep_time": "18 daqiqa"},
            {"id": 11, "name": "Ролл с лососем", "price": 77000, "description": "Сыр.Огурецы.лосось", "prep_time": "16 daqiqa"}
        ]
    },
    "setlar": {
        "name": "🎎 Premium Setlar",
        "emoji": "🎎",
        "products": [
            {"id": 12, "name": "Сет Токио 48шт", "price": 390000, "description": "Дракон ролл + Филадельфия + Темпура", "prep_time": "35 daqiqa"},
            {"id": 13, "name": "Сет Ямамото 32шт", "price": 290000, "description": "Филадельфия + Калифорния", "prep_time": "30 daqiqa"},
            {"id": 14, "name": "Сет Идеал 32шт", "price": 260000, "description": "4 xil rollar", "prep_time": "28 daqiqa"}
        ]
    },
    "ichimliklar": {
        "name": "🥤 Ichimliklar",
        "emoji": "🥤",
        "products": [
            {"id": 15, "name": "Мохито 1л", "price": 45000, "description": "Sovuq mojito", "prep_time": "5 daqiqa"},
            {"id": 16, "name": "Чай Токио", "price": 35000, "description": "Maxsus choy", "prep_time": "3 daqiqa"},
            {"id": 17, "name": "Милкшейк Клубника", "price": 30000, "description": "Qulupnayli milkshake", "prep_time": "7 daqiqa"}
        ]
    }
}

# Ma'lumotlar bazasi
user_data = {}
orders_data = {}
order_counter = 1

# ==================== PREMIUM FUNCTIONS ====================

def send_premium_message(chat_id, text, keyboard=None, remove_keyboard=False):
    """Premium ko'rinishdagi xabar yuborish"""
    try:
        url = BASE_URL + "sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        
        if keyboard:
            data["reply_markup"] = json.dumps(keyboard)
        elif remove_keyboard:
            data["reply_markup"] = json.dumps({"remove_keyboard": True})
            
        response = requests.post(url, json=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"📤 Xabar yuborishda xato: {e}")
        return False

def create_premium_menu(chat_id):
    """Premium menyu yaratish"""
    if str(chat_id) == ADMIN_ID:
        keyboard = {
            "keyboard": [
                ["🍱 Premium Menyu", "🛒 Mening Savatim"],
                ["📦 Buyurtmalarim", "🏪 Biz haqimizda"],
                ["👑 Admin Panel"]
            ],
            "resize_keyboard": True
        }
    else:
        keyboard = {
            "keyboard": [
                ["🍱 Premium Menyu", "🛒 Mening Savatim"],
                ["📦 Buyurtmalarim", "🏪 Biz haqimizda"]
            ],
            "resize_keyboard": True
        }
    return keyboard

def show_premium_categories(chat_id):
    """Premium kategoriyalarni ko'rsatish"""
    keyboard = {
        "keyboard": [
            ["🍜 Issiq Taomlar", "🍣 Premium Rollar"],
            ["🔥 Pishirilgan Rollar", "🎎 Premium Setlar"],
            ["🥤 Ichimliklar", "⬅️ Asosiy menyu"]
        ],
        "resize_keyboard": True
    }
    
    text = f"""
🎌 <b>TOKIO SUSHI PREMIUM MENYU</b> 🍱

⭐ <b>5 ta premium kategoriya</b>
🚚 <b>Yetkazib berish:</b> {DELIVERY_PRICE:,} so'm
⏰ <b>Tayyorlanish vaqti:</b> {PREPARATION_TIME}
🕒 <b>Ish vaqti:</b> {WORK_HOURS}

<b>Marhamat, kerakli bo'limni tanlang:</b>
    """
    send_premium_message(chat_id, text, keyboard)

def show_category_products_premium(chat_id, category_key):
    """Premium mahsulotlarni ko'rsatish"""
    if category_key not in menu_data:
        send_premium_message(chat_id, "❌ Kategoriya topilmadi")
        return
    
    category = menu_data[category_key]
    products = category["products"]
    
    text = f"""
{category['emoji']} <b>{category['name']}</b>
────────────────
    """
    
    for product in products:
        text += f"""
🍣 <b>{product['name']}</b>
💵 <b>Narxi:</b> {product['price']:,} so'm
⏱️ <b>Tayyorlanish:</b> {product['prep_time']}
📝 {product['description']}
────────────────
        """
    
    # Inline keyboard yaratish
    keyboard = {"inline_keyboard": []}
    
    for product in products:
        keyboard["inline_keyboard"].append([{
            "text": f"➕ {product['name']} - {product['price']:,} so'm",
            "callback_data": f"add_{product['id']}"
        }])
    
    keyboard["inline_keyboard"].append([
        {"text": "🛒 Savatni ko'rish", "callback_data": "view_cart"},
        {"text": "📋 Kategoriyalar", "callback_data": "back_to_categories"}
    ])
    
    send_premium_message(chat_id, text, keyboard)

def show_premium_cart(chat_id):
    """Premium savat ko'rinishi"""
    if chat_id not in user_data or "cart" not in user_data[chat_id] or not user_data[chat_id]["cart"]:
        send_premium_message(chat_id, "🛒 <b>Savatingiz hozircha bo'sh</b>")
        return
    
    cart = user_data[chat_id]["cart"]
    total = sum(item['price'] for item in cart)
    total_with_delivery = total + DELIVERY_PRICE
    
    text = f"""
🛒 <b>PREMIUM SAVATINGIZ</b>
────────────────

"""
    
    for i, item in enumerate(cart, 1):
        text += f"{i}. {item['name']} - {item['price']:,} so'm\n"
    
    text += f"""
────────────────
💵 <b>Mahsulotlar:</b> {total:,} so'm
🚚 <b>Yetkazish:</b> {DELIVERY_PRICE:,} so'm
💰 <b>JAMI:</b> {total_with_delivery:,} so'm

⏰ <b>Taxminiy tayyorlik:</b> {PREPARATION_TIME}
    """
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "✅ BUYURTMA BERISH", "callback_data": "place_order"}],
            [{"text": "🗑 Savatni tozalash", "callback_data": "clear_cart"}],
            [{"text": "📝 Davom etish", "callback_data": "back_to_categories"}]
        ]
    }
    
    send_premium_message(chat_id, text, keyboard)

def request_contact_premium(chat_id):
    """Premium telefon so'rash"""
    keyboard = {
        "keyboard": [[{
            "text": "📞 Telefon raqamni yuborish",
            "request_contact": True
        }]],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    
    text = f"""
📞 <b>TELEFON RAQAMINGIZ</b>
────────────────

Buyurtmani yakunlash uchun telefon raqamingizni yuboring.

<b>\"📞 Telefon raqamni yuborish\" tugmasini bosing.</b>
    """
    send_premium_message(chat_id, text, keyboard)

def request_location_premium(chat_id):
    """Premium lokatsiya so'rash"""
    keyboard = {
        "keyboard": [[{
            "text": "📍 Manzilni yuborish",
            "request_location": True
        }]],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    
    text = f"""
📍 <b>MANZILINGIZ</b>
────────────────

Yetkazib berish uchun manzilingizni yuboring.

<b>\"📍 Manzilni yuborish\" tugmasini bosing</b> yoki Google Maps linkini yuboring.
    """
    send_premium_message(chat_id, text, keyboard)

def send_order_confirmation_premium(chat_id, order_id, total, phone, location):
    """Premium buyurtma tasdiqlash"""
    delivery_time = datetime.now() + timedelta(minutes=45)
    
    text = f"""
✅ <b>BUYURTMA QABUL QILINDI!</b>
────────────────

📦 <b>Buyurtma raqami:</b> #{order_id}
💵 <b>Jami summa:</b> {total:,} so'm
📞 <b>Telefon:</b> {phone}
📍 <b>Manzil:</b> {location}
⏰ <b>Yetkazish vaqti:</b> {delivery_time.strftime('%H:%M')}
🚚 <b>Yetkazib berish:</b> {DELIVERY_PRICE:,} so'm

<b>Buyurtmangiz qabul qilindi va tayyorlanmoqda.</b>
📞 <b>Bog'lanish:</b> +998947126030
    """
    
    send_premium_message(chat_id, text, create_premium_menu(chat_id))

def send_order_to_admin_premium(order_id, user_id, total, phone, location, cart):
    """Admin uchun premium buyurtma xabari"""
    maps_link = location if "http" in location else f"https://maps.google.com/?q={location}"
    
    text = f"""
🆕 <b>YANGI PREMIUM BUYURTMA</b> #{order_id}
────────────────

👤 <b>Mijoz ID:</b> {user_id}
📞 <b>Telefon:</b> {phone}
📍 <b>Manzil:</b> <a href='{maps_link}'>Google Mapsda ko'rish</a>
💵 <b>Summa:</b> {total:,} so'm
⏰ <b>Vaqt:</b> {datetime.now().strftime('%H:%M')}

📦 <b>Buyurtma tarkibi:</b>
"""
    
    for item in cart:
        text += f"• {item['name']} - {item['price']:,} so'm\n"
    
    text += f"\n🚚 <b>Yetkazish:</b> {DELIVERY_PRICE:,} so'm"
    text += f"\n💰 <b>Jami:</b> {total + DELIVERY_PRICE:,} so'm"
    
    # Admin uchun boshqaruv tugmalari
    keyboard = {
        "inline_keyboard": [
            [{"text": "✅ Qabul qilish", "callback_data": f"accept_{order_id}"}],
            [{"text": "❌ Bekor qilish", "callback_data": f"cancel_{order_id}"}],
            [{"text": "📞 Bog'lanish", "callback_data": f"contact_{order_id}"}],
            [{"text": "✅ Tayyor", "callback_data": f"ready_{order_id}"}]
        ]
    }
    
    send_premium_message(ADMIN_ID, text, keyboard)

# ==================== ADMIN FUNCTIONS ====================

def admin_panel_premium(chat_id):
    """Premium admin panel"""
    if str(chat_id) != ADMIN_ID:
        send_premium_message(chat_id, "❌ Sizda admin huquqi yo'q")
        return
    
    today = datetime.now().date()
    today_orders = [order for order in orders_data.values() 
                   if datetime.fromisoformat(order['timestamp']).date() == today]
    
    text = f"""
👑 <b>PREMIUM ADMIN PANEL</b>
────────────────

📊 <b>Bugun statistikasi:</b>
🛒 Buyurtmalar: {len(today_orders)} ta
💰 Daromad: {sum(order['total'] for order in today_orders):,} so'm
👥 Faol mijozlar: {len(user_data)} ta

⚡ <b>Boshqaruv:</b>
    """
    
    keyboard = {
        "keyboard": [
            ["📊 Bugun statistikasi", "📈 Haftalik statistika"],
            ["📦 Faol buyurtmalar", "✅ Bajarilgan buyurtmalar"],
            ["👥 Mijozlar bazasi", "💰 Daromad hisoboti"],
            ["⬅️ Foydalanuvchi rejimi"]
        ],
        "resize_keyboard": True
    }
    
    send_premium_message(chat_id, text, keyboard)

# ==================== UPTIME ROBOT INTEGRATION ====================

def keep_alive():
    """UptimeRobot uchun keep-alive"""
    try:
        requests.get(f"https://tokiosushibot.onrender.com/health", timeout=5)
        print("🔄 Keep-alive signal sent")
    except:
        print("⚠️ Keep-alive failed")

def start_keep_alive():
    """Keep-alive ni ishga tushirish"""
    schedule.every(10).minutes.do(keep_alive)
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/')
def home():
    return "🎌 TOKIO SUSHI PREMIUM BOT - 24/7 Faol"

@app.route('/health')
def health_check():
    return {
        "status": "premium_healthy",
        "service": "Tokio Sushi Premium Bot",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0",
        "uptime": "24/7"
    }

# ==================== MAIN BOT LOGIC ====================

def run_bot():
    print("🚀 Tokio Sushi Premium Bot ishga tushdi!")
    
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
                            message = update["message"]
                            text = message.get("text", "")
                            
                            # Start command
                            if text == "/start":
                                welcome_text = """
🎌 <b>TOKIO SUSHI PREMIUM</b> 🍱

🏮 <b>Xush kelibsiz! Premium yapon oshxonasi</b>
⭐ Sifatli mahsulotlar
🚚 Tezkor yetkazib berish
💎 Premium xizmat

<b>Quyidagi menyulardan foydalaning:</b>
                                """
                                send_premium_message(chat_id, welcome_text, create_premium_menu(chat_id))
                            
                            # Boshqa commandlar...
                            # (Qolgan logika avvalgidek, faqat premium funksiyalar bilan)
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Xato: {e}")
            time.sleep(3)

if __name__ == "__main__":
    # Keep-alive ni ishga tushirish
    keep_alive_thread = Thread(target=start_keep_alive, daemon=True)
    keep_alive_thread.start()
    
    # Asosiy botni ishga tushirish
    bot_thread = Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Flask server
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
