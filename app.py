import requests
import json
import time
import os
import re
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
DELIVERY_PRICE = 10000
WORK_HOURS = "11:00 - 02:00"
PREPARATION_TIME = "30-45 daqiqa"
DISCOUNT_PERCENT = 20

# Karta ma'lumotlari
CARD_NUMBER = "9860 3501 4052 5865"
CARD_HOLDER = "SHOKHRUKH Y."

# Tillar
languages = {
    "uz": {
        "menu": "🍱 Premium Menyu",
        "cart": "🛒 Savat",
        "orders": "📦 Mening buyurtmalarim",
        "info": "ℹ️ Ma'lumot",
        "admin": "👑 Admin Panel",
        "main_menu": "🏠 Asosiy menyu",
        "view_cart": "🛒 Savatni ko'rish",
        "clear_cart": "🗑 Savatni tozalash",
        "place_order": "✅ Buyurtma berish",
        "back": "⬅️ Ortga",
        "continue": "➡️ Davom etish",
        "confirm": "✅ Tasdiqlash",
        "cancel": "❌ Bekor qilish",
        "delivery": "🚚 Yetkazib berish",
        "pickup": "🏃 Olib ketish",
        "phone": "📞 Telefon raqam",
        "location": "📍 Manzil",
        "payment": "💳 To'lov",
        "cash": "💵 Naqd pul",
        "card": "💳 Karta",
        "feedback": "💬 Fikr qoldirish",
        "language": "🌐 Tilni o'zgartirish"
    },
    "ru": {
        "menu": "🍱 Премиум Меню",
        "cart": "🛒 Корзина",
        "orders": "📦 Мои заказы",
        "info": "ℹ️ Информация",
        "admin": "👑 Панель администратора",
        "main_menu": "🏠 Главное меню",
        "view_cart": "🛒 Посмотреть корзину",
        "clear_cart": "🗑 Очистить корзину",
        "place_order": "✅ Оформить заказ",
        "back": "⬅️ Назад",
        "continue": "➡️ Продолжить",
        "confirm": "✅ Подтвердить",
        "cancel": "❌ Отменить",
        "delivery": "🚚 Доставка",
        "pickup": "🏃 Самовывоз",
        "phone": "📞 Телефон",
        "location": "📍 Адрес",
        "payment": "💳 Оплата",
        "cash": "💵 Наличные",
        "card": "💳 Карта",
        "feedback": "💬 Оставить отзыв",
        "language": "🌐 Сменить язык"
    }
}

# TO'LIQ MENYU MA'LUMOTLARI - RUS TILIDA
menu_data = {
    "holodnye_rolly": {
        "name_uz": "🍣 Sovuq Rollar",
        "name_ru": "🍣 ХОЛОДНЫЕ РОЛЛЫ",
        "emoji": "🍣",
        "products": [
            {"id": 1, "name": "Филадельфия Голд", "price": 120000, "description": "Сыр.Лосось.Огурец.Угорь.Унаги соус.Тунец.Кунжут.Массаго икра", "prep_time": "20 daqiqa"},
            {"id": 2, "name": "Филадельфия (Тунец)", "price": 90000, "description": "Сыр.Тунец", "prep_time": "15 daqiqa"},
            {"id": 3, "name": "Филадельфия Классик", "price": 80000, "description": "Сыр.Огурецы.Лосось", "prep_time": "12 daqiqa"},
            {"id": 4, "name": "Эби Голд", "price": 110000, "description": "Сыр.Лосось.Креветки в кляре.Огурец.Лук", "prep_time": "18 daqiqa"},
            {"id": 5, "name": "Лосось (гриль)", "price": 93000, "description": "Сыр.Унаги соус.Лосось.Массаго", "prep_time": "15 daqiqa"},
            {"id": 6, "name": "Калифорния с креветками", "price": 80000, "description": "Сыр.Огурец.Креветки тигровые.Массаго красс", "prep_time": "12 daqiqa"},
            {"id": 7, "name": "Калифорния с лососем", "price": 76000, "description": "Сыр.Огурец.Лосось.Массаго красс", "prep_time": "12 daqiqa"},
            {"id": 8, "name": "Калифорния с крабом", "price": 70000, "description": "Сыр.Огурец.Снежный краб.Массаго красный", "prep_time": "12 daqiqa"},
            {"id": 9, "name": "Ролл Огурец", "price": 65000, "description": "Сыр.Стружка тунца.Огурец", "prep_time": "10 daqiqa"},
            {"id": 91, "name": "Ролл в Кунжуте", "price": 50000, "description": "Сыр.Кунжут.Краб", "prep_time": "15 daqiqa"},
            {"id": 92, "name": "Дракон", "price": 75000, "description": "Сыр.Угорь.Огурец", "prep_time": "15 daqiqa"},
            {"id": 93, "name": "Канада GOLD", "price": 85000, "description": "Сыр.Лосось.Огурец.Угорь.Унаги соус.Кунжут", "prep_time": "20 daqiqa"}
        ]
    },
    "zapechennye": {
        "name_uz": "🔥 Pishirilgan Rollar",
        "name_ru": "🔥 ЗАПЕЧЕННЫЕ",
        "emoji": "🔥",
        "products": [
            {"id": 10, "name": "Ролл Филадельфия Стейк", "price": 95000, "description": "Сыр.лосось.огурец.сырная шапка", "prep_time": "18 daqiqa"},
            {"id": 11, "name": "Ролл с креветкой", "price": 80000, "description": "Сыр.Тигровые креветки.сырная шапка.Огурец.кунжут", "prep_time": "16 daqiqa"},
            {"id": 12, "name": "Ролл с угрем", "price": 80000, "description": "Сыр.огурецы.кунжут.сырная шапка.угорь", "prep_time": "16 daqiqa"},
            {"id": 13, "name": "Ролл с крабом", "price": 66000, "description": "Сыр.Огурец.Снежный краб", "prep_time": "14 daqiqa"},
            {"id": 14, "name": "Ролл с лососем", "price": 77000, "description": "Сыр.Огурецы.кунжут,сырная шапка,лосось,унаги соус", "prep_time": "15 daqiqa"},
            {"id": 15, "name": "Ролл Калифорния", "price": 70000, "description": "Сыр.Огурецы.снежный краб.икра массаго.сырная шапка.унаги соус", "prep_time": "14 daqiqa"},
            {"id": 16, "name": "Ролл с курицой", "price": 55000, "description": "Майонез.Салат Айзберг.курица.сырная шапка", "prep_time": "12 daqiqa"},
            {"id": 94, "name": "Лосось", "price": 66000, "description": "Лосось, Кунжут", "prep_time": "15 daqiqa"},
            {"id": 95, "name": "Темпура с крабом", "price": 55000, "description": "Краб.Мойонез.Унаги соус", "prep_time": "15 daqiqa"},
            {"id": 96, "name": "Креветки", "price": 70000, "description": "Креветки, сырная шапка", "prep_time": "15 daqiqa"},
            {"id": 97, "name": "Темпура запеченный", "price": 70000, "description": "Сыр.Краб.Огурец", "prep_time": "15 daqiqa"}
        ]
    },
    "jarennye_rolly": {
        "name_uz": "⚡ Qovurilgan Rollar",
        "name_ru": "⚡ ЖАРЕНЫЕ РОЛЛЫ",
        "emoji": "⚡",
        "products": [
            {"id": 17, "name": "Темпура (Тунец)", "price": 75000, "description": "Огурец.Сыр.Тунец", "prep_time": "15 daqiqa"},
            {"id": 18, "name": "Темпура Угорь", "price": 71000, "description": "Сыр.Огурец.Угорь.Массаго красс.Унаги соус", "prep_time": "15 daqiqa"},
            {"id": 19, "name": "Темпура с креветками", "price": 70000, "description": "Сыр.Огурец.Креветки тигровые.Массаго красс.Унаги соус", "prep_time": "15 daqiqa"},
            {"id": 20, "name": "Темпура с лососем", "price": 66000, "description": "Сыр.Огурец.Лосось.Унаги соус.Кунжут", "prep_time": "14 daqiqa"},
            {"id": 21, "name": "Темпура Курица", "price": 48000, "description": "Айсберг.Майонез.Курица.Унаги соус", "prep_time": "12 daqiqa"},
            {"id": 98, "name": "Ясареные роялы", "price": 71000, "description": "Запеченные роллы с унаги соусом", "prep_time": "15 daqiqa"}
        ]
    },
    "sety": {
        "name_uz": "🎎 Setlar",
        "name_ru": "🎎 СЕТЫ",
        "emoji": "🎎",
        "products": [
            {"id": 22, "name": "Сет Токио 48шт", "price": 390000, "description": "Дракон ролл 8шт + Филадельфия классик 8шт + Темпура Лосось 8шт + Краб Запеченый 16шт + Калифорния Лосось 8шт", "prep_time": "40 daqiqa"},
            {"id": 23, "name": "Сет Ямамото 32шт", "price": 290000, "description": "Филадельфия классик 8шт + Калифорния классик 8шт + Ролл с креветками 8шт + Ролл Чука 8шт", "prep_time": "35 daqiqa"},
            {"id": 24, "name": "Сет Идеал 32шт", "price": 260000, "description": "Филадельфия классик 8шт + Калифорния Кунсут 8шт + Калифорния Черный 8шт + Дракон ролл 8шт", "prep_time": "32 daqiqa"},
            {"id": 25, "name": "Сет Окей 24шт", "price": 200000, "description": "Филадельфия классик 8шт + Запеченый лосось 8шт + Темпура лосось 8шт", "prep_time": "30 daqiqa"},
            {"id": 26, "name": "Сет Сакура 24шт", "price": 180000, "description": "Филадельфия классик 4шт + Канада Голд 4шт + Мини ролл лосось 8шт + Темпура лосось 8шт", "prep_time": "28 daqiqa"},
            {"id": 27, "name": "Сет Классический 32шт", "price": 150000, "description": "Мини ролл лосось 8шт + Мини ролл огурец 8шт + Мини ролл тунец 8шт + Мини ролл краб 8шт", "prep_time": "25 daqiqa"}
        ]
    },
    "sushi_gunkan": {
        "name_uz": "🍱 Sushi va Gunkan",
        "name_ru": "🍱 СУШИ И ГУНКАН",
        "emoji": "🍱",
        "products": [
            {"id": 28, "name": "Гункан Тунец", "price": 30000, "description": "Tunetsli gunkan", "prep_time": "5 daqiqa"},
            {"id": 29, "name": "Суши Тунец", "price": 25000, "description": "Tunetsli sushi", "prep_time": "5 daqiqa"},
            {"id": 30, "name": "Мини Тунец", "price": 34000, "description": "Mini tunets sushi", "prep_time": "5 daqiqa"},
            {"id": 31, "name": "Гункан Лосось", "price": 24000, "description": "Lososli gunkan", "prep_time": "5 daqiqa"},
            {"id": 32, "name": "Суши Лосось", "price": 20000, "description": "Lososli sushi", "prep_time": "5 daqiqa"},
            {"id": 33, "name": "Мини Лосось", "price": 34000, "description": "Mini losos sushi", "prep_time": "5 daqiqa"},
            {"id": 34, "name": "Гункан Угорь", "price": 24000, "description": "Ugorli gunkan", "prep_time": "5 daqiqa"},
            {"id": 35, "name": "Суши Угорь", "price": 23000, "description": "Ugorli sushi", "prep_time": "5 daqiqa"},
            {"id": 36, "name": "Мини Угорь", "price": 34000, "description": "Mini ugor sushi", "prep_time": "5 daqiqa"},
            {"id": 37, "name": "Гункан Массаго", "price": 24000, "description": "Massago gunkan", "prep_time": "5 daqiqa"},
            {"id": 38, "name": "Суши Креветка", "price": 20000, "description": "Qisqichbaqali sushi", "prep_time": "5 daqiqa"},
            {"id": 39, "name": "Мини Краб", "price": 23000, "description": "Mini krab sushi", "prep_time": "5 daqiqa"},
            {"id": 40, "name": "Мини Огурец", "price": 15000, "description": "Mini bodring sushi", "prep_time": "5 daqiqa"}
        ]
    },
    "goryachaya_eda": {
        "name_uz": "🍜 Issiq Taomlar",
        "name_ru": "🍜 ГОРЯЧАЯ ЕДА",
        "emoji": "🍜",
        "products": [
            {"id": 41, "name": "Рамэн Классик", "price": 80000, "description": "An'anaviy yapon rameni", "prep_time": "20 daqiqa"},
            {"id": 42, "name": "Рамэн Токио", "price": 66000, "description": "Maxsus ramen", "prep_time": "25 daqiqa"},
            {"id": 43, "name": "Вок с говядиной", "price": 65000, "description": "Mol go'shti bilan vok", "prep_time": "15 daqiqa"},
            {"id": 44, "name": "Том Ям Токио", "price": 95000, "description": "Taylandcha Tom Yam", "prep_time": "30 daqiqa"},
            {"id": 45, "name": "Куриные крылышки", "price": 35000, "description": "Qovurilgan tovuq qanotchalar", "prep_time": "15 daqiqa"},
            {"id": 46, "name": "Кукси", "price": 40000, "description": "Koreyscha kuksi", "prep_time": "10 daqiqa"},
            {"id": 47, "name": "Вок с курицей", "price": 55000, "description": "Tovuqli vok", "prep_time": "12 daqiqa"},
            {"id": 48, "name": "Том Ям Классик", "price": 70000, "description": "Oddiy Tom Yam", "prep_time": "25 daqiqa"},
            {"id": 49, "name": "Хрустящие баклажаны", "price": 45000, "description": "Qarsildoq baqlajonlar", "prep_time": "15 daqiqa"},
            {"id": 50, "name": "Цезарь с курицей", "price": 45000, "description": "Sezar salati", "prep_time": "10 daqiqa"},
            {"id": 51, "name": "Греческий салат", "price": 50000, "description": "Rukola bilan salat", "prep_time": "8 daqiqa"},
            {"id": 52, "name": "Салат Руккола", "price": 40000, "description": "Rukola salati", "prep_time": "8 daqiqa"},
            {"id": 53, "name": "Мужской Каприз", "price": 40000, "description": "Kapriz salati", "prep_time": "8 daqiqa"},
            {"id": 54, "name": "Чука Салат", "price": 35000, "description": "Fuka salati", "prep_time": "8 daqiqa"},
            {"id": 55, "name": "Тар-Тар", "price": 15000, "description": "Tar-Tar sousi bilan", "prep_time": "5 daqiqa"},
            {"id": 56, "name": "Рамэн", "price": 45000, "description": "Oddiy ramen", "prep_time": "18 daqiqa"}
        ]
    },
    "pizza_burger": {
        "name_uz": "🍕 Pizza va Burger",
        "name_ru": "🍕 ПИЦЦА И БУРГЕР",
        "emoji": "🍕",
        "products": [
            {"id": 57, "name": "Токио Микс 35см", "price": 90000, "description": "Tokio miks pizza 35sm", "prep_time": "25 daqiqa"},
            {"id": 58, "name": "Кази 35см", "price": 90000, "description": "Bazi pizza 35sm", "prep_time": "25 daqiqa"},
            {"id": 59, "name": "Микс 35см", "price": 85000, "description": "Aralash pizza 35sm", "prep_time": "22 daqiqa"},
            {"id": 60, "name": "Пепперони 35см", "price": 80000, "description": "Pishloqli pizza 35sm", "prep_time": "20 daqiqa"},
            {"id": 61, "name": "Кузикорин 35см", "price": 80000, "description": "Kuzidirini pizza 35sm", "prep_time": "20 daqiqa"},
            {"id": 62, "name": "Маргарита 35см", "price": 75000, "description": "Margarita pizza 35sm", "prep_time": "18 daqiqa"},
            {"id": 63, "name": "Гамбургер", "price": 28000, "description": "Gamburger", "prep_time": "10 daqiqa"},
            {"id": 64, "name": "Чизбургер", "price": 33000, "description": "Chizburger", "prep_time": "12 daqiqa"},
            {"id": 65, "name": "Токио Бургер", "price": 37000, "description": "Tokio maxsus burger", "prep_time": "15 daqiqa"},
            {"id": 66, "name": "Куриные крылышки", "price": 35000, "description": "Qovurilgan tovuq qanotchalar", "prep_time": "15 daqiqa"},
            {"id": 67, "name": "Сырные шарики", "price": 22000, "description": "Pishloq shariklari", "prep_time": "8 daqiqa"},
            {"id": 68, "name": "Картофель Фри", "price": 22000, "description": "Qovurilgan kartoshka", "prep_time": "7 daqiqa"},
            {"id": 69, "name": "Клаб Сендвич", "price": 35000, "description": "Klub sendvich", "prep_time": "10 daqiqa"}
        ]
    },
    "napitki": {
        "name_uz": "🥤 Ichimliklar",
        "name_ru": "🥤 НАПИТКИ",
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

def get_uzbekistan_time():
    """O'zbekiston vaqtini olish"""
    return datetime.utcnow() + timedelta(hours=5)

def get_user_language(chat_id):
    """Foydalanuvchi tilini olish"""
    if chat_id not in user_data:
        user_data[chat_id] = {"language": "ru"}
    return user_data[chat_id].get("language", "ru")

def get_text(chat_id, key):
    """Foydalanuvchi tiliga mos matn olish"""
    lang = get_user_language(chat_id)
    return languages[lang].get(key, key)

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
    lang = get_user_language(chat_id)
    
    if str(chat_id) == ADMIN_ID:
        keyboard = {
            "keyboard": [
                [get_text(chat_id, "menu"), get_text(chat_id, "cart")],
                [get_text(chat_id, "orders"), get_text(chat_id, "info")],
                [get_text(chat_id, "admin")]
            ],
            "resize_keyboard": True
        }
    else:
        keyboard = {
            "keyboard": [
                [get_text(chat_id, "menu"), get_text(chat_id, "cart")],
                [get_text(chat_id, "orders"), get_text(chat_id, "info")],
                [get_text(chat_id, "feedback"), get_text(chat_id, "language")]
            ],
            "resize_keyboard": True
        }
    return keyboard

def show_full_menu(chat_id):
    """TO'LIQ MENYU - Foydalanuvchi tilida"""
    lang = get_user_language(chat_id)
    
    if lang == "uz":
        text = f"""
🎌 <b>TOKIO SUSHI PREMIUM - TO'LIQ MENYU</b> 🍱

🎎 <i>Sushi - bu iste'mol qilish mumkin bo'lgan san'at!</i>

⭐ <b>8 ta kategoriya, 98 ta premium mahsulot</b>
🚚 <b>Yetkazib berish:</b> {DELIVERY_PRICE:,} so'm
⏰ <b>Tayyorlanish vaqti:</b> {PREPARATION_TIME}
🕒 <b>Ish vaqti:</b> {WORK_HOURS}
🎁 <b>Har bir buyurtmaga {DISCOUNT_PERCENT}% chegirma!</b>

<b>Kategoriyani tanlang:</b>
"""
    else:
        text = f"""
🎌 <b>TOKIO SUSHI PREMIUM - ПОЛНОЕ МЕНЮ</b> 🍱

🎎 <b><i>Суши - это искусство которое можно сьесть!</i></b>

⭐ <b>8 категорий, 98 премиум продуктов</b>
🚚 <b>Доставка:</b> {DELIVERY_PRICE:,} сум
⏰ <b>Время приготовления:</b> {PREPARATION_TIME}
🕒 <b>Время работы:</b> {WORK_HOURS}
🎁 <b>СКИДКА {DISCOUNT_PERCENT}% НА КАЖДЫЙ ЗАКАЗ!</b>

<b>Выберите категорию:</b>
"""
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "🍣 ХОЛОДНЫЕ РОЛЛЫ", "callback_data": "category_holodnye_rolly"}],
            [{"text": "🔥 ЗАПЕЧЕННЫЕ", "callback_data": "category_zapechennye"}],
            [{"text": "⚡ ЖАРЕНЫЕ РОЛЛЫ", "callback_data": "category_jarennye_rolly"}],
            [{"text": "🎎 СЕТЫ", "callback_data": "category_sety"}],
            [{"text": "🍱 СУШИ И ГУНКАН", "callback_data": "category_sushi_gunkan"}],
            [{"text": "🍜 ГОРЯЧАЯ ЕДА", "callback_data": "category_goryachaya_eda"}],
            [{"text": "🍕 ПИЦЦА И БУРГЕР", "callback_data": "category_pizza_burger"}],
            [{"text": "🥤 НАПИТКИ", "callback_data": "category_napitki"}],
            [{"text": get_text(chat_id, "view_cart"), "callback_data": "view_cart"}],
            [{"text": get_text(chat_id, "main_menu"), "callback_data": "main_menu"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def show_category(chat_id, category_key):
    """Kategoriyani ko'rsatish"""
    lang = get_user_language(chat_id)
    category = menu_data[category_key]
    
    if lang == "uz":
        category_name = category["name_uz"]
    else:
        category_name = category["name_ru"]
    
    text = f"<b>{category['emoji']} {category_name}</b>\n\n"
    
    for product in category["products"]:
        text += f"<b>🍣 {product['name']}</b>\n"
        text += f"<b>💰 {product['price']:,} {'so\'m' if lang == 'uz' else 'сум'}</b>\n"
        text += f"⏱️ {product['prep_time']}\n"
        text += f"📝 {product['description']}\n\n"
    
    keyboard = {"inline_keyboard": []}
    
    # Mahsulot qo'shish tugmalari
    for product in category["products"]:
        keyboard["inline_keyboard"].append([{
            "text": f"➕ {product['name']} - {product['price']:,} {'so\'m' if lang == 'uz' else 'сум'}",
            "callback_data": f"add_{product['id']}"
        }])
    
    # Navigatsiya tugmalari
    keyboard["inline_keyboard"].extend([
        [{"text": get_text(chat_id, "view_cart"), "callback_data": "view_cart"}],
        [{"text": "📋 Полное меню", "callback_data": "show_menu"}],
        [{"text": get_text(chat_id, "main_menu"), "callback_data": "main_menu"}]
    ])
    
    send_message(chat_id, text, keyboard)

def add_to_cart(chat_id, product_id):
    """Mahsulotni savatga qo'shish"""
    lang = get_user_language(chat_id)
    
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
        send_message(chat_id, "❌ Продукт не найден")
        return
    
    # Foydalanuvchi ma'lumotlarini tekshirish
    if chat_id not in user_data:
        user_data[chat_id] = {"cart": {}, "language": "ru"}
    
    if "cart" not in user_data[chat_id]:
        user_data[chat_id]["cart"] = {}
    
    # Savatga qo'shish
    cart = user_data[chat_id]["cart"]
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1
    
    if lang == "uz":
        text = f"""
✅ <b>SAVATGA QO'SHILDI</b>

🍣 {product['name']}
💰 Narxi: {product['price']:,} so'm
⏱️ Tayyorlanish: {product['prep_time']}
🔢 Soni: {cart[product_id]} ta

🛒 Savatingizdagi mahsulotlar: {len(cart)} ta
    """
    else:
        text = f"""
✅ <b>ДОБАВЛЕНО В КОРЗИНУ</b>

🍣 {product['name']}
💰 Цена: {product['price']:,} сум
⏱️ Приготовление: {product['prep_time']}
🔢 Количество: {cart[product_id]} шт

🛒 Товаров в корзине: {len(cart)} шт
    """
    
    keyboard = {
        "inline_keyboard": [
            [{"text": get_text(chat_id, "view_cart"), "callback_data": "view_cart"}],
            [{"text": "📋 Меню", "callback_data": "show_menu"}],
            [{"text": get_text(chat_id, "place_order"), "callback_data": "place_order"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def show_cart(chat_id):
    """Savatni ko'rsatish"""
    lang = get_user_language(chat_id)
    
    if chat_id not in user_data or "cart" not in user_data[chat_id] or not user_data[chat_id]["cart"]:
        if lang == "uz":
            send_message(chat_id, "🛒 <b>Savatingiz bo'sh</b>\n\nMarhamat, menyudan mahsulot tanlang!")
        else:
            send_message(chat_id, "🛒 <b>Ваша корзина пуста</b>\n\nПожалуйста, выберите продукты из меню!")
        return
    
    cart = user_data[chat_id]["cart"]
    total = 0
    items_text = ""
    
    for product_id, quantity in cart.items():
        # Mahsulotni topish
        product = None
        for category in menu_data.values():
            for p in category["products"]:
                if p["id"] == product_id:
                    product = p
                    break
            if product:
                break
        
        if product:
            item_total = product['price'] * quantity
            total += item_total
            if lang == "uz":
                items_text += f"{product['name']} - {quantity} x {product['price']:,} = {item_total:,} so'm\n"
            else:
                items_text += f"{product['name']} - {quantity} x {product['price']:,} = {item_total:,} сум\n"
    
    # 20% chegirma hisoblash
    discount_amount = total * DISCOUNT_PERCENT // 100
    total_with_discount = total - discount_amount
    total_with_delivery = total_with_discount + DELIVERY_PRICE
    
    if lang == "uz":
        text = f"🛒 <b>SAVATINGIZ</b>\n\n{items_text}\n"
        text += f"💵 Mahsulotlar: {total:,} so'm\n"
        text += f"🎁 Chegirma ({DISCOUNT_PERCENT}%): -{discount_amount:,} so'm\n"
        text += f"💳 Chegirma bilan: {total_with_discount:,} so'm\n"
        text += f"🚚 Yetkazish: {DELIVERY_PRICE:,} so'm\n"
        text += f"💰 <b>JAMI: {total_with_delivery:,} so'm</b>\n"
        text += f"⏰ Tayyorlanish: {PREPARATION_TIME}"
    else:
        text = f"🛒 <b>ВАША КОРЗИНА</b>\n\n{items_text}\n"
        text += f"💵 Товары: {total:,} сум\n"
        text += f"🎁 Скидка ({DISCOUNT_PERCENT}%): -{discount_amount:,} сум\n"
        text += f"💳 Со скидкой: {total_with_discount:,} сум\n"
        text += f"🚚 Доставка: {DELIVERY_PRICE:,} сум\n"
        text += f"💰 <b>ИТОГО: {total_with_delivery:,} сум</b>\n"
        text += f"⏰ Время приготовления: {PREPARATION_TIME}"
    
    keyboard = {
        "inline_keyboard": []
    }
    
    # Har bir mahsulot uchun boshqarish tugmalari
    for product_id, quantity in cart.items():
        product = None
        for category in menu_data.values():
            for p in category["products"]:
                if p["id"] == product_id:
                    product = p
                    break
            if product:
                break
        
        if product:
            row = [
                {"text": f"➖", "callback_data": f"dec_{product_id}"},
                {"text": f"{product['name']} ({quantity})", "callback_data": f"info_{product_id}"},
                {"text": f"➕", "callback_data": f"inc_{product_id}"},
                {"text": f"🗑", "callback_data": f"del_{product_id}"}
            ]
            keyboard["inline_keyboard"].append(row)
    
    # Asosiy tugmalar
    keyboard["inline_keyboard"].extend([
        [{"text": get_text(chat_id, "place_order"), "callback_data": "place_order"}],
        [{"text": get_text(chat_id, "clear_cart"), "callback_data": "clear_cart"}],
        [{"text": "📋 Меню", "callback_data": "show_menu"}],
        [{"text": get_text(chat_id, "main_menu"), "callback_data": "main_menu"}]
    ])
    
    send_message(chat_id, text, keyboard)

def change_cart_quantity(chat_id, product_id, action):
    """Savatdagi mahsulot sonini o'zgartirish"""
    lang = get_user_language(chat_id)
    
    if chat_id not in user_data or "cart" not in user_data[chat_id]:
        return
    
    cart = user_data[chat_id]["cart"]
    
    if action == "inc":
        cart[product_id] += 1
    elif action == "dec":
        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            del cart[product_id]
    elif action == "del":
        del cart[product_id]
    
    show_cart(chat_id)

def request_delivery_method(chat_id):
    """Yetkazib berish usulini so'rash"""
    lang = get_user_language(chat_id)
    
    if lang == "uz":
        text = """
🚚 <b>YETKAZIB BERISH USULINI TANLANG</b>

Buyurtmangizni qanday olishni xohlaysiz?

• <b>🏃 Olib ketish</b> - o'zingiz kelib olib ketasiz
• <b>🚚 Yetkazib berish</b> - manzilingizga yetkazib beramiz
        """
    else:
        text = """
🚚 <b>ВЫБЕРИТЕ СПОСОБ ПОЛУЧЕНИЯ</b>

Как вы хотите получить ваш заказ?

• <b>🏃 Самовывоз</b> - заберете сами
• <b>🚚 Доставка</b> - доставим по вашему адресу
        """
    
    keyboard = {
        "keyboard": [
            [get_text(chat_id, "pickup"), get_text(chat_id, "delivery")],
            [get_text(chat_id, "back")]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    
    send_message(chat_id, text, keyboard)

def request_contact_and_location(chat_id, delivery_type):
    """Telefon raqam va lokatsiya so'rash"""
    lang = get_user_language(chat_id)
    
    if delivery_type == "pickup":
        # Faqat telefon so'raymiz
        request_contact(chat_id)
    else:
        # Telefon va lokatsiya so'raymiz
        request_contact(chat_id)

def request_contact(chat_id):
    """Telefon raqam so'rash"""
    lang = get_user_language(chat_id)
    
    # Oldingi ma'lumotlarni tozalash
    if chat_id in user_data:
        user_data[chat_id].pop("phone", None)
        user_data[chat_id].pop("location", None)
        user_data[chat_id].pop("location_type", None)
        user_data[chat_id].pop("delivery_type", None)
    
    if lang == "uz":
        text = """
📞 <b>TELEFON RAQAMINGIZNI YUBORING</b>

Buyurtma berish uchun telefon raqamingizni yuboring.
"📞 Telefon raqamni yuborish" tugmasini bosing.
        """
    else:
        text = """
📞 <b>ОТПРАВЬТЕ ВАШ НОМЕР ТЕЛЕФОНА</b>

Для оформления заказа отправьте ваш номер телефона.
Нажмите кнопку "📞 Отправить номер телефона".
        """
    
    keyboard = {
        "keyboard": [[{
            "text": "📞 Telefon raqamni yuborish",
            "request_contact": True
        }]],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    
    send_message(chat_id, text, keyboard)

def request_location(chat_id):
    """Lokatsiya so'rash"""
    lang = get_user_language(chat_id)
    
    if lang == "uz":
        text = """
📍 <b>MANZILINGIZNI YUBORING</b>

Yetkazib berish uchun manzilingizni yuboring.

"📍 Geolokatsiyani yuborish" tugmasini bosing yoki aniq manzilingizni matn shaklida yozing.

📝 <i>Misol: Qarshi shahar, Amir Temur ko'chasi, 45-uy</i>
        """
    else:
        text = """
📍 <b>ОТПРАВЬТЕ ВАШ АДРЕС</b>

Для доставки отправьте ваш адрес.

Нажмите кнопку "📍 Отправить геолокацию" или напишите точный адрес текстом.

📝 <i>Пример: г. Карши, ул. Амира Темура, дом 45</i>
        """
    
    keyboard = {
        "keyboard": [
            [{
                "text": "📍 Geolokatsiyani yuborish",
                "request_location": True
            }],
            [get_text(chat_id, "back")]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    
    send_message(chat_id, text, keyboard)

def show_feedback_menu(chat_id):
    """Fikr-mulohaza menyusi"""
    lang = get_user_language(chat_id)
    
    if lang == "uz":
        text = """
💬 <b>FIKR-MULOHAZA QOLDIRISH</b>

Tokio Sushi xizmatlarini baholang. 
Sizning fikringiz biz uchun muhim!
        """
    else:
        text = """
💬 <b>ОСТАВИТЬ ОТЗЫВ</b>

Оцените услуги Tokio Sushi.
Ваше мнение важно для нас!
        """
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "⭐️⭐️⭐️⭐️⭐️", "callback_data": "feedback_5"}],
            [{"text": "⭐️⭐️⭐️⭐️", "callback_data": "feedback_4"}],
            [{"text": "⭐️⭐️⭐️", "callback_data": "feedback_3"}],
            [{"text": "⭐️⭐️", "callback_data": "feedback_2"}],
            [{"text": "⭐️", "callback_data": "feedback_1"}],
            [{"text": get_text(chat_id, "back"), "callback_data": "main_menu"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def show_language_menu(chat_id):
    """Tilni o'zgartirish menyusi"""
    lang = get_user_language(chat_id)
    
    if lang == "uz":
        text = """
🌐 <b>TILNI O'ZGARTIRISH</b>

Qulay tilni tanlang:
        """
    else:
        text = """
🌐 <b>СМЕНА ЯЗЫКА</b>

Выберите удобный язык:
        """
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "🇺🇿 O'zbekcha", "callback_data": "lang_uz"}],
            [{"text": "🇷🇺 Русский", "callback_data": "lang_ru"}],
            [{"text": get_text(chat_id, "back"), "callback_data": "main_menu"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def change_language(chat_id, language):
    """Tilni o'zgartirish"""
    if chat_id not in user_data:
        user_data[chat_id] = {}
    
    user_data[chat_id]["language"] = language
    
    if language == "uz":
        text = "✅ Til o'zbekchaga o'zgartirildi"
    else:
        text = "✅ Язык изменен на русский"
    
    send_message(chat_id, text, main_menu(chat_id))

# ... (qolgan funksiyalar avvalgidek, faqat tilga moslashtirilgan)

# ==================== BOT LOGIKASI ====================

def handle_callback(chat_id, callback_data):
    """Callbacklarni qayta ishlash"""
    try:
        if callback_data.startswith("add_"):
            product_id = int(callback_data.split("_")[1])
            add_to_cart(chat_id, product_id)
            
        elif callback_data.startswith("inc_"):
            product_id = int(callback_data.split("_")[1])
            change_cart_quantity(chat_id, product_id, "inc")
            
        elif callback_data.startswith("dec_"):
            product_id = int(callback_data.split("_")[1])
            change_cart_quantity(chat_id, product_id, "dec")
            
        elif callback_data.startswith("del_"):
            product_id = int(callback_data.split("_")[1])
            change_cart_quantity(chat_id, product_id, "del")
            
        elif callback_data == "view_cart":
            show_cart(chat_id)
            
        elif callback_data == "place_order":
            request_delivery_method(chat_id)
            
        elif callback_data == "clear_cart":
            if chat_id in user_data:
                user_data[chat_id]["cart"] = {}
            send_message(chat_id, get_text(chat_id, "clear_cart"), main_menu(chat_id))
            
        elif callback_data == "show_menu":
            show_full_menu(chat_id)
            
        elif callback_data.startswith("category_"):
            category_key = callback_data.split("_", 1)[1]
            show_category(chat_id, category_key)
            
        elif callback_data == "main_menu":
            send_message(chat_id, get_text(chat_id, "main_menu"), main_menu(chat_id))
            
        elif callback_data.startswith("feedback_"):
            rating = int(callback_data.split("_")[1])
            lang = get_user_language(chat_id)
            if lang == "uz":
                send_message(chat_id, f"✅ Baholangiz uchun rahmat! ({rating}/5)")
            else:
                send_message(chat_id, f"✅ Спасибо за вашу оценку! ({rating}/5)")
            send_message(chat_id, get_text(chat_id, "main_menu"), main_menu(chat_id))
            
        elif callback_data.startswith("lang_"):
            language = callback_data.split("_")[1]
            change_language(chat_id, language)
            
        # ... (qolgan callback'lar avvalgidek)
            
    except Exception as e:
        print(f"Callback xatosi: {e}")
        send_message(chat_id, "❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

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
                                welcome_text = f"""
🎌 <b>TOKIO SUSHI PREMIUM</b> 🍱

🏮 <b>Добро пожаловать! Премиум японская кухня</b>
⭐ 98 премиум продуктов
🚚 Быстрая доставка
🎁 <b>СКИДКА {DISCOUNT_PERCENT}% НА КАЖДЫЙ ЗАКАЗ!</b>

📞 Связь: +998 91 211 12 15
                                """
                                send_message(chat_id, welcome_text, main_menu(chat_id))
                            
                            elif text == get_text(chat_id, "menu"):
                                show_full_menu(chat_id)
                            
                            elif text == get_text(chat_id, "cart"):
                                show_cart(chat_id)
                                
                            elif text == get_text(chat_id, "orders"):
                                user_orders = [order for order in orders_data.values() if order["user_id"] == chat_id]
                                if user_orders:
                                    text = "📦 <b>ВАШИ ЗАКАЗЫ</b>\n\n"
                                    for order in user_orders[-5:]:
                                        status_emoji = "✅" if order["status"] == "готов" else "⏳" if order["status"] == "принят" else "❌"
                                        text += f"{status_emoji} #{list(orders_data.keys())[list(orders_data.values()).index(order)]} - {order['total_with_delivery']:,} сум - {order['status']}\n"
                                    send_message(chat_id, text)
                                else:
                                    send_message(chat_id, "📦 У вас еще нет заказов")
                            
                            elif text == get_text(chat_id, "info"):
                                info_text = f"""
🏮 <b>TOKIO SUSHI</b> 🎌

⭐ Премиум японская кухня
🕒 Время работы: {WORK_HOURS}
🚚 Доставка: {PREPARATION_TIME}
💰 Стоимость доставки: {DELIVERY_PRICE:,} сум
🎁 <b>Скидка {DISCOUNT_PERCENT}% на каждый заказ!</b>

📞 Связь: +998 91 211 12 15
📍 Адрес: г. Карши
                                """
                                send_message(chat_id, info_text)
                            
                            elif text == get_text(chat_id, "feedback"):
                                show_feedback_menu(chat_id)
                            
                            elif text == get_text(chat_id, "language"):
                                show_language_menu(chat_id)
                            
                            elif text == get_text(chat_id, "admin") and str(chat_id) == ADMIN_ID:
                                today_orders = len([o for o in orders_data.values() if datetime.fromisoformat(o['timestamp']).date() == get_uzbekistan_time().date()])
                                admin_text = f"""
👑 <b>ПАНЕЛЬ АДМИНИСТРАТОРА</b>

📊 Заказов сегодня: {today_orders} шт
👥 Всего клиентов: {len(user_data)} чел
💰 Всего заказов: {len(orders_data)} шт
🕒 Время: {get_uzbekistan_time().strftime('%H:%M')}
                                """
                                send_message(chat_id, admin_text)
                            
                            elif text == get_text(chat_id, "back") or text == get_text(chat_id, "main_menu"):
                                send_message(chat_id, get_text(chat_id, "main_menu"), main_menu(chat_id))
                            
                            # Yetkazib berish usullari
                            elif text == get_text(chat_id, "pickup"):
                                if chat_id not in user_data:
                                    user_data[chat_id] = {}
                                user_data[chat_id]["delivery_type"] = "pickup"
                                request_contact(chat_id)
                            
                            elif text == get_text(chat_id, "delivery"):
                                if chat_id not in user_data:
                                    user_data[chat_id] = {}
                                user_data[chat_id]["delivery_type"] = "delivery"
                                request_contact(chat_id)
                            
                            # ... (qolgan xabarlarni qayta ishlash avvalgidek)
                            
                        elif "callback_query" in update:
                            callback = update["callback_query"]
                            chat_id = callback["message"]["chat"]["id"]
                            callback_data = callback["data"]
                            
                            handle_callback(chat_id, callback_data)
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Xato: {e}")
            time.sleep(3)

# ... (qolgan kod avvalgidek)

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
