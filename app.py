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

# TO'LIQ MENYU MA'LUMOTLARI
menu_data = {
    "issiq_taomlar": {
        "name": "🍜 Issiq Taomlar",
        "emoji": "🍜",
        "products": [
            {"id": 1, "name": "Рамэн Классик", "price": 80000, "description": "An'anaviy yapon rameni", "prep_time": "20 daqiqa"},
            {"id": 2, "name": "Рамэн Токио", "price": 66000, "description": "Maxsus ramen", "prep_time": "25 daqiqa"},
            {"id": 3, "name": "Вок с говядиной", "price": 65000, "description": "Mol go'shti bilan vok", "prep_time": "15 daqiqa"},
            {"id": 4, "name": "Том Ям Токио", "price": 95000, "description": "Taylandcha Tom Yam", "prep_time": "30 daqiqa"},
            {"id": 5, "name": "Куриные крылышки", "price": 35000, "description": "Qovurilgan tovuq qanotchalar", "prep_time": "15 daqiqa"},
            {"id": 6, "name": "Кукси", "price": 40000, "description": "Koreyscha kuksi", "prep_time": "10 daqiqa"},
            {"id": 7, "name": "Вок с курицей", "price": 55000, "description": "Tovuqli vok", "prep_time": "12 daqiqa"},
            {"id": 8, "name": "Том Ям Классик", "price": 70000, "description": "Oddiy Tom Yam", "prep_time": "25 daqiqa"},
            {"id": 9, "name": "Хрустящие баклажаны", "price": 45000, "description": "Qarsildoq baqlajonlar", "prep_time": "15 daqiqa"},
            {"id": 10, "name": "Цезарь с курицей", "price": 45000, "description": "Sezar salati", "prep_time": "10 daqiqa"},
            {"id": 11, "name": "Греческий салат", "price": 50000, "description": "Rukola bilan salat", "prep_time": "8 daqiqa"},
            {"id": 12, "name": "Салат Руккола", "price": 40000, "description": "Rukola salati", "prep_time": "8 daqiqa"},
            {"id": 13, "name": "Мужской Каприз", "price": 40000, "description": "Kapriz salati", "prep_time": "8 daqiqa"},
            {"id": 14, "name": "Чука Салат", "price": 35000, "description": "Fuka salati", "prep_time": "8 daqiqa"},
            {"id": 15, "name": "Тар-Тар", "price": 15000, "description": "Tar-Tar sousi bilan", "prep_time": "5 daqiqa"},
            {"id": 16, "name": "Рамэн", "price": 45000, "description": "Oddiy ramen", "prep_time": "18 daqiqa"}
        ]
    },
    "pizza_burger": {
        "name": "🍕 Pizza va Burger",
        "emoji": "🍕",
        "products": [
            {"id": 17, "name": "Токио Микс 35см", "price": 90000, "description": "Tokio miks pizza 35sm", "prep_time": "25 daqiqa"},
            {"id": 18, "name": "Кази 35см", "price": 90000, "description": "Bazi pizza 35sm", "prep_time": "25 daqiqa"},
            {"id": 19, "name": "Микс 35см", "price": 85000, "description": "Aralash pizza 35sm", "prep_time": "22 daqiqa"},
            {"id": 20, "name": "Пепперони 35см", "price": 80000, "description": "Pishloqli pizza 35sm", "prep_time": "20 daqiqa"},
            {"id": 21, "name": "Кузикорин 35см", "price": 80000, "description": "Kuzidirini pizza 35sm", "prep_time": "20 daqiqa"},
            {"id": 22, "name": "Маргарита 35см", "price": 75000, "description": "Margarita pizza 35sm", "prep_time": "18 daqiqa"},
            {"id": 23, "name": "Гамбургер", "price": 28000, "description": "Gamburger", "prep_time": "10 daqiqa"},
            {"id": 24, "name": "Чизбургер", "price": 33000, "description": "Chizburger", "prep_time": "12 daqiqa"},
            {"id": 25, "name": "Токио Бургер", "price": 37000, "description": "Tokio maxsus burger", "prep_time": "15 daqiqa"},
            {"id": 26, "name": "Куриные крылышки", "price": 35000, "description": "Qovurilgan tovuq qanotchalar", "prep_time": "15 daqiqa"},
            {"id": 27, "name": "Сырные шарики", "price": 22000, "description": "Pishloq shariklari", "prep_time": "8 daqiqa"},
            {"id": 28, "name": "Картофель Фри", "price": 22000, "description": "Qovurilgan kartoshka", "prep_time": "7 daqiqa"},
            {"id": 29, "name": "Клаб Сендвич", "price": 35000, "description": "Klub sendvich", "prep_time": "10 daqiqa"}
        ]
    },
    "sovuq_rollar": {
        "name": "🍣 Sovuq Rollar",
        "emoji": "🍣",
        "products": [
            {"id": 30, "name": "Филадельфия Голд", "price": 120000, "description": "Сыр.Лосось.Огурец.Угорь.Унаги соус.Тунец.Кунжут.Массаго икра", "prep_time": "20 daqiqa"},
            {"id": 31, "name": "Филадельфия (Тунец)", "price": 90000, "description": "Сыр.Тунец", "prep_time": "15 daqiqa"},
            {"id": 32, "name": "Филадельфия Классик", "price": 80000, "description": "Сыр.Огурецы.Лосось", "prep_time": "12 daqiqa"},
            {"id": 33, "name": "Эби Голд", "price": 110000, "description": "Сыр.Лосось.Креветки в кляре.Огурец.Лук", "prep_time": "18 daqiqa"},
            {"id": 34, "name": "Лосось (гриль)", "price": 93000, "description": "Сыр.Унаги соус.Лосось.Массаго", "prep_time": "15 daqiqa"},
            {"id": 35, "name": "Калифорния с креветками", "price": 80000, "description": "Сыр.Огурец.Креветки тигровые.Массаго красс", "prep_time": "12 daqiqa"},
            {"id": 36, "name": "Калифорния с лососем", "price": 76000, "description": "Сыр.Огурец.Лосось.Массаго красс", "prep_time": "12 daqiqa"},
            {"id": 37, "name": "Калифорния с крабом", "price": 70000, "description": "Сыр.Огурец.Снежный краб.Массаго красный", "prep_time": "12 daqiqa"},
            {"id": 38, "name": "Ролл Огурец", "price": 65000, "description": "Сыр.Стружка тунца.Огурец", "prep_time": "10 daqiqa"}
        ]
    },
    "pishirilgan_rollar": {
        "name": "🔥 Pishirilgan Rollar",
        "emoji": "🔥",
        "products": [
            {"id": 39, "name": "Ролл Филадельфия Стейк", "price": 95000, "description": "Сыр.лосось.огурец.сырная шапка", "prep_time": "18 daqiqa"},
            {"id": 40, "name": "Ролл с креветкой", "price": 80000, "description": "Сыр.Тигровые креветки.сырная шапка.Огурец.кунжут", "prep_time": "16 daqiqa"},
            {"id": 41, "name": "Ролл с угрем", "price": 80000, "description": "Сыр.огурецы.кунжут.сырная шапка.угорь", "prep_time": "16 daqiqa"},
            {"id": 42, "name": "Ролл с крабом", "price": 66000, "description": "Сыр.Огурец.Снежный краб", "prep_time": "14 daqiqa"},
            {"id": 43, "name": "Ролл с лососем", "price": 77000, "description": "Сыр.Огурецы.кунжут,сырная шапка,лосось,унаги соус", "prep_time": "15 daqiqa"},
            {"id": 44, "name": "Ролл Калифорния", "price": 70000, "description": "Сыр.Огурецы.снежный краб.икра массаго.сырная шапка.унаги соус", "prep_time": "14 daqiqa"},
            {"id": 45, "name": "Ролл с курицой", "price": 55000, "description": "Майонез.Салат Айзберг.курица.сырная шапка", "prep_time": "12 daqiqa"}
        ]
    },
    "qovurilgan_rollar": {
        "name": "⚡ Qovurilgan Rollar",
        "emoji": "⚡",
        "products": [
            {"id": 46, "name": "Темпура (Тунец)", "price": 75000, "description": "Огурец.Сыр.Тунец", "prep_time": "15 daqiqa"},
            {"id": 47, "name": "Темпура Угорь", "price": 71000, "description": "Сыр.Огурец.Угорь.Массаго красс.Унаги соус", "prep_time": "15 daqiqa"},
            {"id": 48, "name": "Темпура с креветками", "price": 70000, "description": "Сыр.Огурец.Креветки тигровые.Массаго красс.Унаги соус", "prep_time": "15 daqiqa"},
            {"id": 49, "name": "Темпура с лососем", "price": 66000, "description": "Сыр.Огурец.Лосось.Унаги соус.Кунжут", "prep_time": "14 daqiqa"},
            {"id": 50, "name": "Темпура Курица", "price": 48000, "description": "Айсберг.Майонез.Курица.Унаги соус", "prep_time": "12 daqiqa"}
        ]
    },
    "sushi_gunkan": {
        "name": "🍱 Sushi va Gunkan",
        "emoji": "🍱",
        "products": [
            {"id": 51, "name": "Гункан Тунец", "price": 30000, "description": "Tunetsli gunkan", "prep_time": "5 daqiqa"},
            {"id": 52, "name": "Суши Тунец", "price": 25000, "description": "Tunetsli sushi", "prep_time": "5 daqiqa"},
            {"id": 53, "name": "Мини Тунец", "price": 34000, "description": "Mini tunets sushi", "prep_time": "5 daqiqa"},
            {"id": 54, "name": "Гункан Лосось", "price": 24000, "description": "Lososli gunkan", "prep_time": "5 daqiqa"},
            {"id": 55, "name": "Суши Лосось", "price": 20000, "description": "Lososli sushi", "prep_time": "5 daqiqa"},
            {"id": 56, "name": "Мини Лосось", "price": 34000, "description": "Mini losos sushi", "prep_time": "5 daqiqa"},
            {"id": 57, "name": "Гункан Угорь", "price": 24000, "description": "Ugorli gunkan", "prep_time": "5 daqiqa"},
            {"id": 58, "name": "Суши Угорь", "price": 23000, "description": "Ugorli sushi", "prep_time": "5 daqiqa"},
            {"id": 59, "name": "Мини Угорь", "price": 34000, "description": "Mini ugor sushi", "prep_time": "5 daqiqa"},
            {"id": 60, "name": "Гункан Массаго", "price": 24000, "description": "Massago gunkan", "prep_time": "5 daqiqa"},
            {"id": 61, "name": "Суши Креветка", "price": 20000, "description": "Qisqichbaqali sushi", "prep_time": "5 daqiqa"},
            {"id": 62, "name": "Мини Краб", "price": 23000, "description": "Mini krab sushi", "prep_time": "5 daqiqa"},
            {"id": 63, "name": "Мини Огурец", "price": 15000, "description": "Mini bodring sushi", "prep_time": "5 daqiqa"}
        ]
    },
    "setlar": {
        "name": "🎎 Setlar",
        "emoji": "🎎",
        "products": [
            {"id": 64, "name": "Сет Токио 48шт", "price": 390000, "description": "Дракон ролл 8шт + Филадельфия классик 8шт + Темпура Лосось 8шт + Краб Запеченый 16шт + Калифорния Лосось 8шт", "prep_time": "40 daqiqa"},
            {"id": 65, "name": "Сет Ямамото 32шт", "price": 290000, "description": "Филадельфия классик 8шт + Калифорния классик 8шт + Ролл с креветками 8шт + Ролл Чука 8шт", "prep_time": "35 daqiqa"},
            {"id": 66, "name": "Сет Идеал 32шт", "price": 260000, "description": "Филадельфия классик 8шт + Калифорния Кунжут 8шт + Калифорния Черный 8шт + Дракон ролл 8шт", "prep_time": "32 daqiqa"},
            {"id": 67, "name": "Сет Окей 24шт", "price": 200000, "description": "Филадельфия классик 8шт + Запеченый лосось 8шт + Темпура лосось 8шт", "prep_time": "30 daqiqa"},
            {"id": 68, "name": "Сет Сакура 24шт", "price": 180000, "description": "Филадельфия классик 4шт + Канада Голд 4шт + Мини ролл лосось 8шт + Темпура лосось 8шт", "prep_time": "28 daqiqa"},
            {"id": 69, "name": "Сет Классический 32шт", "price": 150000, "description": "Мини ролл лосось 8шт + Мини ролл огурец 8шт + Мини ролл тунец 8шт + Мини ролл краб 8шт", "prep_time": "25 daqiqa"}
        ]
    },
    "ichimliklar": {
        "name": "🥤 Ichimliklar",
        "emoji": "🥤",
        "products": [
            {"id": 70, "name": "Мохито 1л", "price": 45000, "description": "Sovuq mojito", "prep_time": "3 daqiqa"},
            {"id": 71, "name": "Мохито 0.7л", "price": 25000, "description": "Sovuq mojito", "prep_time": "3 daqiqa"},
            {"id": 72, "name": "Мохито 0.5л", "price": 20000, "description": "Sovuq mojito", "prep_time": "3 daqiqa"},
            {"id": 73, "name": "Чай Чудо", "price": 35000, "description": "Maxsus choy", "prep_time": "2 daqiqa"},
            {"id": 74, "name": "Чай Токио", "price": 35000, "description": "Tokio maxsus choy", "prep_time": "2 daqiqa"},
            {"id": 75, "name": "Чай Фруктовый", "price": 35000, "description": "Mevali choy", "prep_time": "2 daqiqa"},
            {"id": 76, "name": "Чай Тархун", "price": 35000, "description": "Tarxun choyi", "prep_time": "2 daqiqa"},
            {"id": 77, "name": "Чай Багини", "price": 35000, "description": "Rayhon choyi", "prep_time": "2 daqiqa"},
            {"id": 78, "name": "Чай Каркаде", "price": 30000, "description": "Karkade choyi", "prep_time": "2 daqiqa"},
            {"id": 79, "name": "Чай Лимон", "price": 25000, "description": "Limonli choy", "prep_time": "2 daqiqa"},
            {"id": 80, "name": "Милкшейк Клубника", "price": 30000, "description": "Qulupnayli milkshake", "prep_time": "5 daqiqa"},
            {"id": 81, "name": "Милкшейк Сникерс", "price": 30000, "description": "Snickers milkshake", "prep_time": "5 daqiqa"},
            {"id": 82, "name": "Милкшейк Банан", "price": 30000, "description": "Bananli milkshake", "prep_time": "5 daqiqa"},
            {"id": 83, "name": "Милкшейк Орео", "price": 30000, "description": "Oreo milkshake", "prep_time": "5 daqiqa"},
            {"id": 84, "name": "Милкшейк Киви", "price": 30000, "description": "Kinder milkshake", "prep_time": "5 daqiqa"},
            {"id": 85, "name": "Кола 1л", "price": 14000, "description": "Gazlangan ichimlik 1L", "prep_time": "1 daqiqa"},
            {"id": 86, "name": "Фанта 1л", "price": 14000, "description": "Gazlangan ichimlik 1L", "prep_time": "1 daqiqa"},
            {"id": 87, "name": "Фюсти 1л", "price": 13000, "description": "Gazlangan ichimlik 1L", "prep_time": "1 daqiqa"},
            {"id": 88, "name": "Кола-Фанта Ж/Б", "price": 10000, "description": "Kola 0.5L", "prep_time": "1 daqiqa"},
            {"id": 89, "name": "Вода Без Газа", "price": 8000, "description": "Gazsiz suv", "prep_time": "1 daqiqa"},
            {"id": 90, "name": "Сок", "price": 19000, "description": "Tabiiy sok", "prep_time": "1 daqiqa"}
        ]
    }
}

# Ma'lumotlar bazasi
user_data = {}
orders_data = {}
order_counter = 1

# ==================== ASOSIY FUNKSIYALAR ====================

def send_message(chat_id, text, keyboard=None):
    """Xabar yuborish"""
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
        response = requests.post(url, json=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Xabar yuborishda xato: {e}")
        return False

def main_menu(chat_id):
    """Asosiy menyu"""
    if str(chat_id) == ADMIN_ID:
        keyboard = {
            "keyboard": [
                ["🍱 Premium Menyu", "🛒 Savat"],
                ["📦 Mening buyurtmalarim", "ℹ️ Ma'lumot"],
                ["👑 Admin Panel"]
            ],
            "resize_keyboard": True
        }
    else:
        keyboard = {
            "keyboard": [
                ["🍱 Premium Menyu", "🛒 Savat"],
                ["📦 Mening buyurtmalarim", "ℹ️ Ma'lumot"]
            ],
            "resize_keyboard": True
        }
    return keyboard

def show_categories(chat_id):
    """Kategoriyalarni ko'rsatish"""
    keyboard = {
        "keyboard": [
            ["🍜 Issiq Taomlar", "🍕 Pizza va Burger"],
            ["🍣 Sovuq Rollar", "🔥 Pishirilgan Rollar"],
            ["⚡ Qovurilgan Rollar", "🍱 Sushi va Gunkan"],
            ["🎎 Setlar", "🥤 Ichimliklar"],
            ["⬅️ Asosiy menyu"]
        ],
        "resize_keyboard": True
    }
    
    text = f"""
🎌 <b>TOKIO SUSHI PREMIUM MENYU</b> 🍱

⭐ <b>8 ta kategoriya, 90 ta mahsulot</b>
🚚 <b>Yetkazib berish:</b> {DELIVERY_PRICE:,} so'm
⏰ <b>Tayyorlanish vaqti:</b> {PREPARATION_TIME}
🕒 <b>Ish vaqti:</b> {WORK_HOURS}

<b>Marhamat, kerakli bo'limni tanlang:</b>
    """
    send_message(chat_id, text, keyboard)

def show_category_products(chat_id, category_key, start_index=0):
    """Kategoriya mahsulotlarini ko'rsatish"""
    if category_key not in menu_data:
        send_message(chat_id, "❌ Kategoriya topilmadi")
        return
    
    category = menu_data[category_key]
    products = category["products"]
    
    # Sahifalash
    end_index = min(start_index + 4, len(products))
    current_products = products[start_index:end_index]
    
    text = f"{category['emoji']} <b>{category['name']}</b>\n\n"
    
    for product in current_products:
        text += f"🍣 {product['name']} - {product['price']:,} so'm\n"
        text += f"⏱️ {product['prep_time']} | {product['description']}\n\n"
    
    # Inline keyboard
    keyboard = {"inline_keyboard": []}
    
    for product in current_products:
        keyboard["inline_keyboard"].append([{
            "text": f"➕ {product['name']} - {product['price']:,} so'm",
            "callback_data": f"add_{product['id']}"
        }])
    
    # Sahifalash tugmalari
    nav_buttons = []
    if start_index > 0:
        nav_buttons.append({"text": "⬅️ Oldingi", "callback_data": f"prev_{category_key}_{start_index-4}"})
    if end_index < len(products):
        nav_buttons.append({"text": "Keyingi ➡️", "callback_data": f"next_{category_key}_{end_index}"})
    
    if nav_buttons:
        keyboard["inline_keyboard"].append(nav_buttons)
    
    keyboard["inline_keyboard"].append([
        {"text": "🛒 Savat", "callback_data": "view_cart"},
        {"text": "📋 Menyu", "callback_data": "back_to_categories"}
    ])
    
    send_message(chat_id, text, keyboard)

def add_to_cart(chat_id, product_id):
    """Mahsulotni savatga qo'shish"""
    # Mahsulotni topish
    product = None
    for category in menu_data.values():
        for p in category["products"]:
            if p["id"] == product_id:
                product = p
                break
        if product:
            break
    
    if not product:
        send_message(chat_id, "❌ Mahsulot topilmadi")
        return
    
    # Foydalanuvchi ma'lumotlarini tekshirish
    if chat_id not in user_data:
        user_data[chat_id] = {"cart": []}
    
    if "cart" not in user_data[chat_id]:
        user_data[chat_id]["cart"] = []
    
    # Savatga qo'shish
    user_data[chat_id]["cart"].append(product)
    
    text = f"""
✅ <b>SAVATGA QO'SHILDI</b>

🍣 {product['name']}
💰 Narxi: {product['price']:,} so'm
⏱️ Tayyorlanish: {product['prep_time']}

🛒 Savatingizdagi mahsulotlar: {len(user_data[chat_id]['cart'])} ta
    """
    send_message(chat_id, text)

def show_cart(chat_id):
    """Savatni ko'rsatish"""
    if chat_id not in user_data or "cart" not in user_data[chat_id] or not user_data[chat_id]["cart"]:
        send_message(chat_id, "🛒 <b>Savatingiz bo'sh</b>")
        return
    
    cart = user_data[chat_id]["cart"]
    total = sum(item['price'] for item in cart)
    total_with_delivery = total + DELIVERY_PRICE
    
    text = "🛒 <b>SAVATINGIZ</b>\n\n"
    for i, item in enumerate(cart, 1):
        text += f"{i}. {item['name']} - {item['price']:,} so'm\n"
    
    text += f"\n💵 Mahsulotlar: {total:,} so'm"
    text += f"\n🚚 Yetkazish: {DELIVERY_PRICE:,} so'm"
    text += f"\n💰 <b>JAMI: {total_with_delivery:,} so'm</b>"
    text += f"\n⏰ Tayyorlanish: {PREPARATION_TIME}"
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "✅ BUYURTMA BERISH", "callback_data": "place_order"}],
            [{"text": "🗑 Savatni tozalash", "callback_data": "clear_cart"}],
            [{"text": "📝 Davom etish", "callback_data": "back_to_categories"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def request_contact(chat_id):
    """Telefon raqam so'rash"""
    keyboard = {
        "keyboard": [[{
            "text": "📞 Telefon raqamni yuborish",
            "request_contact": True
        }]],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    
    text = """
📞 <b>TELEFON RAQAMINGIZNI YUBORING</b>

Buyurtma berish uchun telefon raqamingizni yuboring.
"📞 Telefon raqamni yuborish" tugmasini bosing.
    """
    send_message(chat_id, text, keyboard)

def request_location(chat_id):
    """Lokatsiya so'rash"""
    keyboard = {
        "keyboard": [[{
            "text": "📍 Lokatsiyani yuborish",
            "request_location": True
        }]],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    
    text = """
📍 <b>MANZILINGIZNI YUBORING</b>

Yetkazib berish uchun manzilingizni yuboring.
"📍 Lokatsiyani yuborish" tugmasini bosing yoki Google Maps linkini yuboring.
    """
    send_message(chat_id, text, keyboard)

def process_order(chat_id):
    """Buyurtmani qayta ishlash"""
    if chat_id not in user_data or "cart" not in user_data[chat_id] or not user_data[chat_id]["cart"]:
        send_message(chat_id, "❌ Savatingiz bo'sh")
        return
    
    # Telefon va manzilni tekshirish
    user_info = user_data.get(chat_id, {})
    
    if "phone" not in user_info:
        request_contact(chat_id)
        return
    
    if "location" not in user_info:
        request_location(chat_id)
        return
    
    # Buyurtmani saqlash
    global order_counter
    cart = user_data[chat_id]["cart"]
    total = sum(item['price'] for item in cart)
    total_with_delivery = total + DELIVERY_PRICE
    
    order_id = order_counter
    order_counter += 1
    
    orders_data[order_id] = {
        "user_id": chat_id,
        "user_phone": user_info["phone"],
        "user_location": user_info["location"],
        "items": cart.copy(),
        "total": total,
        "total_with_delivery": total_with_delivery,
        "status": "yangi",
        "timestamp": datetime.now().isoformat()
    }
    
    # Savatni tozalash
    user_data[chat_id]["cart"] = []
    
    # Mijozga xabar
    delivery_time = datetime.now() + timedelta(minutes=45)
    text = f"""
✅ <b>BUYURTMA QABUL QILINDI!</b>

📦 Buyurtma raqami: #{order_id}
💰 Jami summa: {total_with_delivery:,} so'm
📞 Telefon: {user_info['phone']}
📍 Manzil: {user_info['location']}
⏰ Yetkazish vaqti: {delivery_time.strftime('%H:%M')}
🚚 Yetkazib berish: {DELIVERY_PRICE:,} so'm

📞 Bog'lanish: +998947126030
    """
    send_message(chat_id, text, main_menu(chat_id))
    
    # Adminga xabar
    maps_link = user_info['location']
    if "http" not in maps_link and "maps" not in maps_link:
        maps_link = f"https://maps.google.com/?q={maps_link}"
    
    admin_text = f"""
🆕 <b>YANGI BUYURTMA</b> #{order_id}

👤 Mijoz ID: {chat_id}
📞 Telefon: {user_info['phone']}
📍 Manzil: <a href='{maps_link}'>Google Maps</a>
💵 Mahsulotlar: {total:,} so'm
🚚 Yetkazish: {DELIVERY_PRICE:,} so'm
💰 Jami: {total_with_delivery:,} so'm
⏰ Vaqt: {datetime.now().strftime('%H:%M')}

📦 Buyurtma:
"""
    for item in cart:
        admin_text += f"• {item['name']} - {item['price']:,} so'm\n"
    
    admin_keyboard = {
        "inline_keyboard": [
            [{"text": "✅ Qabul qilish", "callback_data": f"accept_{order_id}"}],
            [{"text": "❌ Bekor qilish", "callback_data": f"cancel_{order_id}"}],
            [{"text": "✅ Tayyor", "callback_data": f"ready_{order_id}"}],
            [{"text": "📞 Bog'lanish", "callback_data": f"contact_{order_id}"}]
        ]
    }
    
    send_message(ADMIN_ID, admin_text, admin_keyboard)

def handle_callback(chat_id, callback_data):
    """Callbacklarni qayta ishlash"""
    try:
        if callback_data.startswith("add_"):
            product_id = int(callback_data.split("_")[1])
            add_to_cart(chat_id, product_id)
            
        elif callback_data == "view_cart":
            show_cart(chat_id)
            
        elif callback_data == "place_order":
            process_order(chat_id)
            
        elif callback_data == "clear_cart":
            if chat_id in user_data:
                user_data[chat_id]["cart"] = []
            send_message(chat_id, "🗑 Savat tozalandi", main_menu(chat_id))
            
        elif callback_data == "back_to_categories":
            show_categories(chat_id)
            
        elif callback_data.startswith("prev_") or callback_data.startswith("next_"):
            parts = callback_data.split("_")
            action = parts[0]
            category_key = parts[1]
            start_index = int(parts[2])
            
            show_category_products(chat_id, category_key, start_index)
            
        elif callback_data.startswith("accept_"):
            if str(chat_id) == ADMIN_ID:
                order_id = int(callback_data.split("_")[1])
                if order_id in orders_data:
                    orders_data[order_id]["status"] = "qabul_qilindi"
                    user_id = orders_data[order_id]["user_id"]
                    send_message(user_id, f"✅ #{order_id} buyurtmangiz qabul qilindi va tayyorlanmoqda!")
                    send_message(chat_id, f"✅ #{order_id} buyurtma qabul qilindi")
            
        elif callback_data.startswith("ready_"):
            if str(chat_id) == ADMIN_ID:
                order_id = int(callback_data.split("_")[1])
                if order_id in orders_data:
                    orders_data[order_id]["status"] = "tayyor"
                    user_id = orders_data[order_id]["user_id"]
                    send_message(user_id, f"🎉 #{order_id} buyurtmangiz tayyor! Yetkazib berishmoqda...")
                    send_message(chat_id, f"✅ #{order_id} buyurtma tayyor deb belgilandi")
            
        elif callback_data.startswith("cancel_"):
            if str(chat_id) == ADMIN_ID:
                order_id = int(callback_data.split("_")[1])
                if order_id in orders_data:
                    orders_data[order_id]["status"] = "bekor_qilindi"
                    user_id = orders_data[order_id]["user_id"]
                    send_message(user_id, f"❌ #{order_id} buyurtmangiz bekor qilindi. Iltimos, qaytadan urinib ko'ring.")
                    send_message(chat_id, f"❌ #{order_id} buyurtma bekor qilindi")
                    
    except Exception as e:
        print(f"Callback xatosi: {e}")
        send_message(chat_id, "❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

# ==================== UPTIME ROBOT ====================

def keep_alive():
    """UptimeRobot uchun keep-alive"""
    try:
        requests.get("https://tokiosushibot.onrender.com/health", timeout=5)
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
    return {"status": "healthy", "service": "Tokio Sushi Premium Bot", "timestamp": datetime.now().isoformat()}

@app.route('/ping')
def ping():
    return "pong"

# ==================== ASOSIY BOT LOGIKASI ====================

def run_bot():
    print("🚀 Tokio Sushi Premium Bot ishga tushdi!")
    
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
                            message = update["message"]
                            text = message.get("text", "")
                            
                            if text == "/start":
                                welcome_text = """
🎌 <b>TOKIO SUSHI PREMIUM</b> 🍱

🏮 <b>Xush kelibsiz! Premium yapon oshxonasi</b>
⭐ 90 ta mahsulot
🚚 Tezkor yetkazib berish
💎 Premium xizmat

📞 Bog'lanish: +998947126030
                                """
                                send_message(chat_id, welcome_text, main_menu(chat_id))
                            
                            elif text == "🍱 Premium Menyu":
                                show_categories(chat_id)
                            
                            elif text == "🛒 Savat":
                                show_cart(chat_id)
                                
                            elif text == "📦 Mening buyurtmalarim":
                                user_orders = [order for order in orders_data.values() if order["user_id"] == chat_id]
                                if user_orders:
                                    text = "📦 <b>SIZNING BUYURTMALARINGIZ</b>\n\n"
                                    for order in user_orders[-5:]:
                                        status_emoji = "✅" if order["status"] == "tayyor" else "⏳" if order["status"] == "qabul_qilindi" else "❌"
                                        text += f"{status_emoji} #{list(orders_data.keys())[list(orders_data.values()).index(order)]} - {order['total_with_delivery']:,} so'm - {order['status']}\n"
                                    send_message(chat_id, text)
                                else:
                                    send_message(chat_id, "📦 Siz hali buyurtma bermagansiz")
                            
                            elif text == "ℹ️ Ma'lumot":
                                info_text = f"""
🏮 <b>TOKIO SUSHI</b> 🎌

⭐ Premium yapon oshxonasi
🕒 Ish vaqti: {WORK_HOURS}
🚚 Yetkazib berish: {PREPARATION_TIME}
💰 Yetkazish narxi: {DELIVERY_PRICE:,} so'm

📞 Bog'lanish: +998947126030
📍 Manzil: Toshkent shahar
                                """
                                send_message(chat_id, info_text)
                            
                            elif text == "👑 Admin Panel" and str(chat_id) == ADMIN_ID:
                                today_orders = len([o for o in orders_data.values() if datetime.fromisoformat(o['timestamp']).date() == datetime.now().date()])
                                admin_text = f"""
👑 <b>ADMIN PANEL</b>

📊 Bugun buyurtmalar: {today_orders} ta
👥 Jami mijozlar: {len(user_data)} ta
💰 Jami buyurtmalar: {len(orders_data)} ta
🕒 Vaqt: {datetime.now().strftime('%H:%M')}
                                """
                                send_message(chat_id, admin_text)
                            
                            elif text == "⬅️ Asosiy menyu":
                                send_message(chat_id, "🏠 Asosiy menyu", main_menu(chat_id))
                            
                            # Kategoriyalar
                            elif text in ["🍜 Issiq Taomlar", "🍕 Pizza va Burger", "🍣 Sovuq Rollar", 
                                        "🔥 Pishirilgan Rollar", "⚡ Qovurilgan Rollar", "🍱 Sushi va Gunkan",
                                        "🎎 Setlar", "🥤 Ichimliklar"]:
                                category_map = {
                                    "🍜 Issiq Taomlar": "issiq_taomlar",
                                    "🍕 Pizza va Burger": "pizza_burger",
                                    "🍣 Sovuq Rollar": "sovuq_rollar", 
                                    "🔥 Pishirilgan Rollar": "pishirilgan_rollar",
                                    "⚡ Qovurilgan Rollar": "qovurilgan_rollar",
                                    "🍱 Sushi va Gunkan": "sushi_gunkan",
                                    "🎎 Setlar": "setlar",
                                    "🥤 Ichimliklar": "ichimliklar"
                                }
                                show_category_products(chat_id, category_map[text])
                            
                            # Telefon qabul qilish
                            elif "contact" in message:
                                contact = message["contact"]
                                phone = contact.get("phone_number", "")
                                
                                if chat_id not in user_data:
                                    user_data[chat_id] = {}
                                user_data[chat_id]["phone"] = phone
                                send_message(chat_id, f"✅ Telefon raqamingiz qabul qilindi: {phone}")
                                request_location(chat_id)
                            
                            # Lokatsiya qabul qilish
                            elif "location" in message:
                                location = message["location"]
                                lat = location["latitude"]
                                lon = location["longitude"]
                                maps_url = f"https://maps.google.com/?q={lat},{lon}"
                                
                                if chat_id not in user_data:
                                    user_data[chat_id] = {}
                                user_data[chat_id]["location"] = maps_url
                                send_message(chat_id, f"✅ Manzilingiz qabul qilindi!\n📍 {maps_url}")
                                
                                if "cart" in user_data[chat_id] and user_data[chat_id]["cart"]:
                                    send_message(chat_id, "✅ Endi buyurtma berishingiz mumkin! \"🛒 Savat\" tugmasini bosing.", main_menu(chat_id))
                            
                            # Google Maps linkini qabul qilish
                            elif "maps.google.com" in text or "goo.gl/maps" in text:
                                if chat_id not in user_data:
                                    user_data[chat_id] = {}
                                user_data[chat_id]["location"] = text
                                send_message(chat_id, f"✅ Manzilingiz qabul qilindi!\n📍 {text}")
                                
                                if "cart" in user_data[chat_id] and user_data[chat_id]["cart"]:
                                    send_message(chat_id, "✅ Endi buyurtma berishingiz mumkin! \"🛒 Savat\" tugmasini bosing.", main_menu(chat_id))
                        
                        elif "callback_query" in update:
                            callback = update["callback_query"]
                            chat_id = callback["message"]["chat"]["id"]
                            callback_data = callback["data"]
                            
                            handle_callback(chat_id, callback_data)
            
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
