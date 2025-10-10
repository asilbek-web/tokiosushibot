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
DISCOUNT_PERCENT = 20  # 20% chegirma

# Karta ma'lumotlari
CARD_NUMBER = "9860 3501 4052 5865"
CARD_HOLDER = "SHOKHRUKH Y."

# TO'LIQ MENYU MA'LUMOTLARI - RUS TILIDA VA RASMLAR BILAN
menu_data = {
    "holodnye_rolly": {
        "name": "🍣 ХОЛОДНЫЕ РОЛЛЫ",
        "emoji": "🍣",
        "products": [
            {"id": 1, "name": "Филадельфия Голд", "price": 120000, "description": "Сыр.Лосось.Огурец.Угорь.Унаги соус.Тунец.Кунжут.Массаго икра", "prep_time": "20 daqiqa", "image": "https://example.com/images/filadelfiya_gold.jpg"},
            {"id": 2, "name": "Филадельфия (Тунец)", "price": 90000, "description": "Сыр.Тунец", "prep_time": "15 daqiqa", "image": "https://example.com/images/filadelfiya_tunets.jpg"},
            {"id": 3, "name": "Филадельфия Классик", "price": 80000, "description": "Сыр.Огурецы.Лосось", "prep_time": "12 daqiqa", "image": "https://example.com/images/filadelfiya_classic.jpg"},
            {"id": 4, "name": "Эби Голд", "price": 110000, "description": "Сыр.Лосось.Креветки в кляре.Огурец.Лук", "prep_time": "18 daqiqa", "image": "https://example.com/images/ebi_gold.jpg"},
            {"id": 5, "name": "Лосось (гриль)", "price": 93000, "description": "Сыр.Унаги соус.Лосось.Массаго", "prep_time": "15 daqiqa", "image": "https://example.com/images/losos_grill.jpg"},
            {"id": 6, "name": "Калифорния с креветками", "price": 80000, "description": "Сыр.Огурец.Креветки тигровые.Массаго красс", "prep_time": "12 daqiqa", "image": "https://example.com/images/california_krevetka.jpg"},
            {"id": 7, "name": "Калифорния с лососем", "price": 76000, "description": "Сыр.Огурец.Лосось.Массаго красс", "prep_time": "12 daqiqa", "image": "https://example.com/images/california_losos.jpg"},
            {"id": 8, "name": "Калифорния с крабом", "price": 70000, "description": "Сыр.Огурец.Снежный краб.Массаго красный", "prep_time": "12 daqiqa", "image": "https://example.com/images/california_krab.jpg"},
            {"id": 9, "name": "Ролл Огурец", "price": 65000, "description": "Сыр.Стружка тунца.Огурец", "prep_time": "10 daqiqa", "image": "https://example.com/images/roll_ogurec.jpg"},
            {"id": 91, "name": "Ролл в Кунжуте", "price": 50000, "description": "Сыр.Кунжут.Краб", "prep_time": "15 daqiqa", "image": "https://example.com/images/roll_kunjut.jpg"},
            {"id": 92, "name": "Дракон", "price": 75000, "description": "Сыр.Угорь.Огурец", "prep_time": "15 daqiqa", "image": "https://example.com/images/drakon.jpg"},
            {"id": 93, "name": "Канада GOLD", "price": 85000, "description": "Сыр.Лосось.Огурец.Угорь.Унаги соус.Кунжут", "prep_time": "20 daqiqa", "image": "https://example.com/images/kanada_gold.jpg"}
        ]
    },
    "zapechennye": {
        "name": "🔥 ЗАПЕЧЕННЫЕ",
        "emoji": "🔥",
        "products": [
            {"id": 10, "name": "Ролл Филадельфия Стейк", "price": 95000, "description": "Сыр.лосось.огурец.сырная шапка", "prep_time": "18 daqiqa", "image": "https://example.com/images/roll_filadelfiya_steak.jpg"},
            {"id": 11, "name": "Ролл с креветкой", "price": 80000, "description": "Сыр.Тигровые креветки.сырная шапка.Огурец.кунжут", "prep_time": "16 daqiqa", "image": "https://example.com/images/roll_krevetka.jpg"},
            {"id": 12, "name": "Ролл с угрем", "price": 80000, "description": "Сыр.огурецы.кунжут.сырная шапка.угорь", "prep_time": "16 daqiqa", "image": "https://example.com/images/roll_ugor.jpg"},
            {"id": 13, "name": "Ролл с крабом", "price": 66000, "description": "Сыр.Огурец.Снежный краб", "prep_time": "14 daqiqa", "image": "https://example.com/images/roll_krab.jpg"},
            {"id": 14, "name": "Ролл с лососем", "price": 77000, "description": "Сыр.Огурецы.кунжут,сырная шапка,лосось,унаги соус", "prep_time": "15 daqiqa", "image": "https://example.com/images/roll_losos.jpg"},
            {"id": 15, "name": "Ролл Калифорния", "price": 70000, "description": "Сыр.Огурецы.снежный краб.икра массаго.сырная шапка.унаги соус", "prep_time": "14 daqiqa", "image": "https://example.com/images/roll_california.jpg"},
            {"id": 16, "name": "Ролл с курицей", "price": 55000, "description": "Майонез.Салат Айзберг.курица.сырная шапка", "prep_time": "12 daqiqa", "image": "https://example.com/images/roll_kurica.jpg"},
            {"id": 94, "name": "Лосось", "price": 66000, "description": "Лосось, Кунжут", "prep_time": "15 daqiqa", "image": "https://example.com/images/losos.jpg"},
            {"id": 95, "name": "Темпура с крабом", "price": 55000, "description": "Краб.Мойонез.Унаги соус", "prep_time": "15 daqiqa", "image": "https://example.com/images/tempura_krab.jpg"},
            {"id": 96, "name": "Креветки", "price": 70000, "description": "Креветки, сырная шапка", "prep_time": "15 daqiqa", "image": "https://example.com/images/krevetki.jpg"},
            {"id": 97, "name": "Темпура запеченный", "price": 70000, "description": "Сыр.Краб.Огурец", "prep_time": "15 daqiqa", "image": "https://example.com/images/tempura_zapechenny.jpg"}
        ]
    },
    # ... qolgan kategoriyalar ham shu tartibda to'ldiriladi
    # Bu yerda faqat bir kategoriya ko'rsatilgan, qolganlari ham xuddi shunday
}

# Ma'lumotlar bazasi
user_data = {}
orders_data = {}
order_counter = 1

# ==================== YANGI FUNKSIYALAR ====================

def send_photo(chat_id, photo_url, caption=None, keyboard=None):
    """Rasm yuborish"""
    try:
        url = BASE_URL + "sendPhoto"
        data = {
            "chat_id": chat_id,
            "photo": photo_url
        }
        if caption:
            data["caption"] = caption
            data["parse_mode"] = "HTML"
        if keyboard:
            data["reply_markup"] = json.dumps(keyboard)
        
        response = requests.post(url, json=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Rasm yuborishda xato: {e}")
        return False

def show_product_with_image(chat_id, product_id):
    """Mahsulotni rasm bilan ko'rsatish"""
    product = None
    category_name = ""
    cat_key = ""
    
    # Mahsulotni qidirish
    for category_key, category in menu_data.items():
        for p in category["products"]:
            if p["id"] == product_id:
                product = p
                category_name = category["name"]
                cat_key = category_key
                break
        if product:
            break
    
    if not product:
        send_message(chat_id, "❌ Mahsulot topilmadi")
        return
    
    # Matn tayyorlash
    caption = f"""
📸 <b>{product['name']}</b>

💰 <b>Narxi:</b> {product['price']:,} so'm
⏱️ <b>Tayyorlanish vaqti:</b> {product['prep_time']}
📝 <b>Tarkibi:</b> {product['description']}
🏷️ <b>Kategoriya:</b> {category_name}

🎁 <b>Har bir buyurtmada {DISCOUNT_PERCENT}% chegirma!</b>
    """
    
    # Keyboard tayyorlash
    keyboard = {
        "inline_keyboard": [
            [{"text": "🛒 Savatga qo'shish", "callback_data": f"add_{product_id}"}],
            [{"text": "📋 Kategoriyaga qaytish", "callback_data": f"category_{cat_key}"}],
            [{"text": "🍽 Bosh menyu", "callback_data": "show_menu"}]
        ]
    }
    
    # Rasm mavjud bo'lsa, rasm bilan yuborish
    if product.get('image'):
        send_photo(chat_id, product['image'], caption, keyboard)
    else:
        # Rasm bo'lmasa, oddiy xabar
        send_message(chat_id, caption, keyboard)

# ==================== MAVJUD FUNKSIYALAR YANGILANDI ====================

def get_uzbekistan_time():
    """O'zbekiston vaqtini olish"""
    return datetime.utcnow() + timedelta(hours=5)

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
                ["🍽 Mazali Menyu", "🛒 Savat"],
                ["📦 Mening buyurtmalarim", "ℹ️ Ma'lumot"],
                ["👑 Admin Panel"]
            ],
            "resize_keyboard": True
        }
    else:
        keyboard = {
            "keyboard": [
                ["🍽 Mazali Menyu", "🛒 Savat"],
                ["📦 Mening buyurtmalarim", "ℹ️ Ma'lumot"]
            ],
            "resize_keyboard": True
        }
    return keyboard

def show_full_menu(chat_id):
    """MAZALI MENYU - RUS TILIDA"""
    text = f"""
🎌 <b>TOKIO SUSHI - МАЗАЛИ МЕНЮ</b> 🍱

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
            [{"text": "🛒 Корзина", "callback_data": "view_cart"}],
            [{"text": "🏠 Главное меню", "callback_data": "main_menu"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def show_category(chat_id, category_key):
    """Kategoriyani ko'rsatish - ENDI RASM KO'RSATISH TUGMASI BILAN"""
    category = menu_data[category_key]
    text = f"<b>{category['emoji']} {category['name']}</b>\n\n"
    text += "📸 <i>Har bir mahsulotni rasmini ko'rish uchun 'Rasmni ko\'rish' tugmasini bosing</i>\n\n"
    
    for product in category["products"]:
        text += f"<b>🍣 {product['name']}</b>\n"
        text += f"<b>💰 {product['price']:,} сум</b>\n"
        text += f"⏱️ {product['prep_time']}\n\n"
    
    keyboard = {"inline_keyboard": []}
    
    # Mahsulotlar uchun tugmalar - Rasm ko'rish va qo'shish
    for product in category["products"]:
        keyboard["inline_keyboard"].append([
            {
                "text": f"📸 {product['name']}",
                "callback_data": f"show_{product['id']}"
            },
            {
                "text": f"🛒 Qo'shish",
                "callback_data": f"add_{product['id']}"
            }
        ])
    
    # Navigatsiya tugmalari
    keyboard["inline_keyboard"].extend([
        [{"text": "🛒 Корзина", "callback_data": "view_cart"}],
        [{"text": "📋 Полное меню", "callback_data": "show_menu"}],
        [{"text": "🏠 Главное меню", "callback_data": "main_menu"}]
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
        send_message(chat_id, "❌ Продукт не найден")
        return
    
    # Foydalanuvchi ma'lumotlarini tekshirish
    if chat_id not in user_data:
        user_data[chat_id] = {"cart": []}
    
    if "cart" not in user_data[chat_id]:
        user_data[chat_id]["cart"] = []
    
    # Savatga qo'shish
    user_data[chat_id]["cart"].append(product)
    
    text = f"""
✅ <b>ДОБАВЛЕНО В КОРЗИНУ</b>

🍣 {product['name']}
💰 Цена: {product['price']:,} сум
⏱️ Приготовление: {product['prep_time']}

🛒 Товаров в корзине: {len(user_data[chat_id]['cart'])} шт
    """
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "🛒 Посмотреть корзину", "callback_data": "view_cart"}],
            [{"text": "📋 Меню", "callback_data": "show_menu"}],
            [{"text": "✅ Оформить заказ", "callback_data": "place_order"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def show_cart(chat_id):
    """Savatni ko'rsatish"""
    if chat_id not in user_data or "cart" not in user_data[chat_id] or not user_data[chat_id]["cart"]:
        send_message(chat_id, "🛒 <b>Ваша корзина пуста</b>\n\nПожалуйста, выберите продукты из меню!")
        return
    
    cart = user_data[chat_id]["cart"]
    total = sum(item['price'] for item in cart)
    
    # 20% chegirma hisoblash
    discount_amount = total * DISCOUNT_PERCENT // 100
    total_with_discount = total - discount_amount
    total_with_delivery = total_with_discount + DELIVERY_PRICE
    
    text = "🛒 <b>ВАША КОРЗИНА</b>\n\n"
    for i, item in enumerate(cart, 1):
        text += f"{i}. {item['name']} - {item['price']:,} сум\n"
    
    text += f"\n💵 Товары: {total:,} сум"
    text += f"\n🎁 Скидка ({DISCOUNT_PERCENT}%): -{discount_amount:,} сум"
    text += f"\n💳 Со скидкой: {total_with_discount:,} сум"
    text += f"\n🚚 Доставка: {DELIVERY_PRICE:,} сум"
    text += f"\n💰 <b>ИТОГО: {total_with_delivery:,} сум</b>"
    text += f"\n⏰ Время приготовления: {PREPARATION_TIME}"
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "✅ ОФОРМИТЬ ЗАКАЗ", "callback_data": "place_order"}],
            [{"text": "🗑 Очистить корзина", "callback_data": "clear_cart"}],
            [{"text": "📋 Посмотреть меню", "callback_data": "show_menu"}],
            [{"text": "🏠 Главное меню", "callback_data": "main_menu"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def handle_callback(chat_id, callback_data):
    """Callbacklarni qayta ishlash - YANGI: show_ HANDLER QO'SHILDI"""
    try:
        if callback_data.startswith("add_"):
            product_id = int(callback_data.split("_")[1])
            add_to_cart(chat_id, product_id)
            
        elif callback_data.startswith("show_"):
            product_id = int(callback_data.split("_")[1])
            show_product_with_image(chat_id, product_id)
            
        elif callback_data == "view_cart":
            show_cart(chat_id)
            
        elif callback_data == "place_order":
            process_order(chat_id)
            
        elif callback_data == "clear_cart":
            if chat_id in user_data:
                user_data[chat_id]["cart"] = []
            send_message(chat_id, "🗑 Корзина очищена", main_menu(chat_id))
            
        elif callback_data == "show_menu":
            show_full_menu(chat_id)
            
        elif callback_data.startswith("category_"):
            category_key = callback_data.split("_", 1)[1]
            show_category(chat_id, category_key)
            
        elif callback_data == "main_menu":
            send_message(chat_id, "🏠 Главное меню", main_menu(chat_id))
            
        elif callback_data.startswith("payment_done_"):
            order_id = int(callback_data.split("_")[2])
            text = f"""
✅ <b>ИНФОРМАЦИЯ ОБ ОПЛАТЕ ПРИНЯТА</b>

📦 Номер заказа: #{order_id}
💳 Пожалуйста, отправьте скриншот чека.

⏳ После подтверждения оплаты ваш заказ будет приготовлен.
📞 Связь: +998 91 211 12 15
            """
            send_message(chat_id, text, main_menu(chat_id))
            
        elif callback_data.startswith("accept_"):
            if str(chat_id) == ADMIN_ID:
                order_id = int(callback_data.split("_")[1])
                if order_id in orders_data:
                    orders_data[order_id]["status"] = "принят"
                    user_id = orders_data[order_id]["user_id"]
                    send_message(user_id, f"✅ Заказ #{order_id} принят и готовится!")
                    send_message(chat_id, f"✅ Заказ #{order_id} принят")
            
        elif callback_data.startswith("ready_"):
            if str(chat_id) == ADMIN_ID:
                order_id = int(callback_data.split("_")[1])
                if order_id in orders_data:
                    orders_data[order_id]["status"] = "готов"
                    user_id = orders_data[order_id]["user_id"]
                    send_message(user_id, f"🎉 Заказ #{order_id} готов! Доставляется...")
                    send_message(chat_id, f"✅ Заказ #{order_id} отмечен как готовый")
            
        elif callback_data.startswith("cancel_"):
            if str(chat_id) == ADMIN_ID:
                order_id = int(callback_data.split("_")[1])
                if order_id in orders_data:
                    orders_data[order_id]["status"] = "отменен"
                    user_id = orders_data[order_id]["user_id"]
                    send_message(user_id, f"❌ Заказ #{order_id} отменен. Пожалуйста, попробуйте снова.")
                    send_message(chat_id, f"❌ Заказ #{order_id} отменен")
            
        elif callback_data.startswith("contact_"):
            if str(chat_id) == ADMIN_ID:
                order_id = int(callback_data.split("_")[1])
                if order_id in orders_data:
                    user_id = orders_data[order_id]["user_id"]
                    user_phone = orders_data[order_id]["user_phone"]
                    send_message(chat_id, f"📞 Номер телефона клиента для заказа #{order_id}: {user_phone}")
            
        elif callback_data.startswith("maps_"):
            if str(chat_id) == ADMIN_ID:
                order_id = int(callback_data.split("_")[1])
                if order_id in orders_data:
                    send_maps_links_to_admin(order_id)
            
        elif callback_data.startswith("cash_paid_"):
            if str(chat_id) == ADMIN_ID:
                order_id = int(callback_data.split("_")[2])
                if order_id in orders_data:
                    orders_data[order_id]["payment_status"] = "оплачено"
                    orders_data[order_id]["status"] = "принят"
                    user_id = orders_data[order_id]["user_id"]
                    send_message(user_id, f"✅ Оплата для заказа #{order_id} получена и заказ готовится!")
                    send_message(chat_id, f"✅ Оплата для заказа #{order_id} подтверждена")
                    
    except Exception as e:
        print(f"Ошибка callback: {e}")
        send_message(chat_id, "❌ Произошла ошибка. Пожалуйста, попробуйте снова.")

# ==================== QOLGAN FUNKSIYALAR O'ZGARMADI ====================

def request_contact_and_location(chat_id):
    """Telefon raqam va lokatsiya so'rash - HAR BUYURTMA UCHUN ALohida"""
    request_contact(chat_id)

def request_contact(chat_id):
    """Telefon raqam so'rash"""
    if chat_id in user_data:
        user_data[chat_id].pop("phone", None)
        user_data[chat_id].pop("location", None)
        user_data[chat_id].pop("location_type", None)
    
    keyboard = {
        "keyboard": [[{
            "text": "📞 Отправить номер телефона",
            "request_contact": True
        }]],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    
    text = """
📞 <b>ОТПРАВЬТЕ ВАШ НОМЕР ТЕЛЕФОНА</b>

Для оформления заказа отправьте ваш номер телефона.
Нажмите кнопку "📞 Отправить номер телефона".
    """
    send_message(chat_id, text, keyboard)

def request_location(chat_id):
    """Lokatsiya so'rash - Google Maps va Yandex Maps"""
    keyboard = {
        "keyboard": [
            [{
                "text": "📍 Через Google Maps",
                "request_location": True
            }],
            [{
                "text": "🌐 Отправить Yandex Maps ссылку"
            }],
            ["🏠 Главное меню"]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    
    text = """
📍 <b>ОТПРАВЬТЕ ВАШ АДРЕС</b>

Для доставки отправьте ваш адрес.

<b>Варианты:</b>
• "📍 Через Google Maps" - отправьте вашу геолокацию
• "🌐 Отправить Yandex Maps ссылку" - отправьте ссылку Yandex Maps
• Или напишите точный адрес текстом

📝 <i>Пример: г. Карши, ул. Амира Темура, дом 45</i>
    """
    send_message(chat_id, text, keyboard)

def request_payment_method(chat_id):
    """To'lov usulini so'rash"""
    keyboard = {
        "keyboard": [
            ["💳 Оплата картой", "💵 Наличные"],
            ["🏠 Главное меню"]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    
    text = """
💳 <b>ВЫБЕРИТЕ СПОСОБ ОПЛАТЫ</b>

Пожалуйста, выберите удобный способ оплаты:

• <b>💳 Оплата картой</b> - перевод на карту
• <b>💵 Наличные</b> - наличными при доставке
    """
    send_message(chat_id, text, keyboard)

def show_card_payment(chat_id, order_id):
    """Karta orqali to'lov ma'lumotlari"""
    order = orders_data[order_id]
    
    text = f"""
💳 <b>ОПЛАТА КАРТОЙ</b>

📦 Номер заказа: #{order_id}
💰 Сумма оплаты: {order['total_with_delivery']:,} сум

<b>Данные карты:</b>
💳 Номер карты: <code>{CARD_NUMBER}</code>
👤 Владелец карты: {CARD_HOLDER}

💡 <b>После оплаты отправьте скриншот чека</b>

✅ После подтверждения оплаты ваш заказ будет приготовлен.
    """
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "✅ Я оплатил", "callback_data": f"payment_done_{order_id}"}],
            [{"text": "🏠 Главное меню", "callback_data": "main_menu"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def confirm_cash_payment(chat_id, order_id):
    """Naqd to'lovni tasdiqlash"""
    order = orders_data[order_id]
    
    text = f"""
💵 <b>ОПЛАТА НАЛИЧНЫМИ ПОДТВЕРЖДЕНА</b>

📦 Номер заказа: #{order_id}
💰 Сумма оплаты: {order['total_with_delivery']:,} сум
✅ Способ оплаты: Наличные

🎉 Ваш заказ принят и готовится!
⏰ Время приготовления: {PREPARATION_TIME}

📞 Связь: +998 91 211 12 15
    """
    
    # Buyurtma holatini yangilash
    orders_data[order_id]["status"] = "принят"
    orders_data[order_id]["payment_method"] = "наличные"
    orders_data[order_id]["payment_status"] = "ожидается"
    
    send_message(chat_id, text, main_menu(chat_id))
    
    # Adminga naqd to'lov haqida xabar
    admin_text = f"""
💵 <b>ОПЛАТА НАЛИЧНЫМИ - ЗАКАЗ #{order_id}</b>

👤 ID клиента: {order['user_id']}
📞 Телефон: {order['user_phone']}
💰 Сумма: {order['total_with_delivery']:,} сум
📍 Адрес: {order['user_location']}
🗺️ Тип карты: {order['location_type']}

✅ Способ оплаты: Наличные
🔄 Статус: Ожидается оплата
    """
    
    admin_keyboard = {
        "inline_keyboard": [
            [{"text": "✅ Оплата получена", "callback_data": f"cash_paid_{order_id}"}],
            [{"text": "❌ Отменить", "callback_data": f"cancel_{order_id}"}]
        ]
    }
    
    send_message(ADMIN_ID, admin_text, admin_keyboard)

def create_maps_links(location, location_type):
    """Google Maps va Yandex Maps linklarini yaratish"""
    if location_type == "google_maps":
        if "http" in location:
            google_link = location
            # Google Maps linkidan Yandex Maps linkini yaratish
            if "?q=" in location:
                coords = location.split("?q=")[1]
                yandex_link = f"https://yandex.com/maps/?text={coords}"
            else:
                yandex_link = f"https://yandex.com/maps/?text={location}"
        else:
            google_link = f"https://maps.google.com/?q={location}"
            yandex_link = f"https://yandex.com/maps/?text={location}"
    
    elif location_type == "yandex_maps":
        if "http" in location:
            yandex_link = location
            # Yandex Maps linkidan Google Maps linkini yaratish
            if "?text=" in location:
                address = location.split("?text=")[1]
                google_link = f"https://maps.google.com/?q={address}"
            else:
                google_link = f"https://maps.google.com/?q={location}"
        else:
            google_link = f"https://maps.google.com/?q={location}"
            yandex_link = f"https://yandex.com/maps/?text={location}"
    
    else:  # text location
        google_link = f"https://maps.google.com/?q={location}"
        yandex_link = f"https://yandex.com/maps/?text={location}"
    
    return google_link, yandex_link

def send_order_to_admin(order_id):
    """Buyurtmani adminga yuborish - IKKALA XARITA HAM"""
    order = orders_data[order_id]
    
    # Xarita linklarini yaratish
    google_link, yandex_link = create_maps_links(
        order["user_location"], 
        order["location_type"]
    )
    
    payment_method = order.get("payment_method", "Не выбран")
    payment_status = order.get("payment_status", "ожидается")
    
    admin_text = f"""
🆕 <b>НОВЫЙ ЗАКАЗ</b> #{order_id}

👤 ID клиента: {order['user_id']}
📞 Телефон: {order['user_phone']}
📍 Адрес: {order['user_location']}
🗺️ Тип карты: {order['location_type']}

🗺️ <b>ССЫЛКИ НА КАРТЫ:</b>
📍 Google Maps: {google_link}
🌐 Yandex Maps: {yandex_link}

💵 Товары: {order['total']:,} сум
🎁 Скидка ({DISCOUNT_PERCENT}%): -{order['discount_amount']:,} сум
💳 Со скидкой: {order['total_with_discount']:,} сум
🚚 Доставка: {DELIVERY_PRICE:,} сум
💰 <b>ИТОГО: {order['total_with_delivery']:,} сум</b>

💳 Способ оплаты: {payment_method}
🔄 Статус оплаты: {payment_status}
⏰ Время: {get_uzbekistan_time().strftime('%H:%M')}

📦 <b>Состав заказа:</b>
"""
    for i, item in enumerate(order["items"], 1):
        admin_text += f"{i}. {item['name']} - {item['price']:,} сум\n"
    
    admin_keyboard = {
        "inline_keyboard": [
            [{"text": "✅ Принять", "callback_data": f"accept_{order_id}"}],
            [{"text": "❌ Отменить", "callback_data": f"cancel_{order_id}"}],
            [{"text": "✅ Заказ Готов", "callback_data": f"ready_{order_id}"}],
            [{"text": "📞 Связаться с клиентом", "callback_data": f"contact_{order_id}"}],
            [{"text": "🗺️ Ссылки на карты", "callback_data": f"maps_{order_id}"}]
        ]
    }
    
    send_message(ADMIN_ID, admin_text, admin_keyboard)

def send_maps_links_to_admin(order_id):
    """Adminga alohida xarita linklarini yuborish"""
    order = orders_data[order_id]
    
    google_link, yandex_link = create_maps_links(
        order["user_location"], 
        order["location_type"]
    )
    
    maps_text = f"""
🗺️ <b>ССЫЛКИ НА КАРТЫ ДЛЯ ЗАКАЗА #{order_id}</b>

📍 <b>Google Maps:</b>
{google_link}

🌐 <b>Yandex Maps:</b>
{yandex_link}

👤 Клиент: {order['user_phone']}
📍 Адрес: {order['user_location']}
    """
    
    send_message(ADMIN_ID, maps_text)

def process_order(chat_id):
    """Buyurtmani qayta ishlash - HAR SAFAR TELEFON VA LOKATSIYA SO'RASH"""
    if chat_id not in user_data or "cart" not in user_data[chat_id] or not user_data[chat_id]["cart"]:
        send_message(chat_id, "❌ Ваша корзина пуста")
        return
    
    # Har safar telefon va lokatsiya so'rash
    request_contact_and_location(chat_id)

def create_order_from_cart(chat_id):
    """Savatdagi mahsulotlardan buyurtma yaratish"""
    if chat_id not in user_data or "cart" not in user_data[chat_id] or not user_data[chat_id]["cart"]:
        send_message(chat_id, "❌ Ваша корзина пуста")
        return
    
    if "phone" not in user_data[chat_id] or "location" not in user_data[chat_id]:
        send_message(chat_id, "❌ Информация о телефоне или адресе недостаточна")
        return
    
    # Buyurtmani saqlash
    global order_counter
    cart = user_data[chat_id]["cart"]
    total = sum(item['price'] for item in cart)
    
    # 20% chegirma hisoblash
    discount_amount = total * DISCOUNT_PERCENT // 100
    total_with_discount = total - discount_amount
    total_with_delivery = total_with_discount + DELIVERY_PRICE
    
    order_id = order_counter
    order_counter += 1
    
    orders_data[order_id] = {
        "user_id": chat_id,
        "user_phone": user_data[chat_id]["phone"],
        "user_location": user_data[chat_id]["location"],
        "location_type": user_data[chat_id]["location_type"],
        "items": cart.copy(),
        "total": total,
        "discount_amount": discount_amount,
        "total_with_discount": total_with_discount,
        "total_with_delivery": total_with_delivery,
        "status": "новый",
        "payment_method": None,
        "payment_status": "ожидается",
        "timestamp": get_uzbekistan_time().isoformat()
    }
    
    # Savatni tozalash
    user_data[chat_id]["cart"] = []
    
    # To'lov usulini so'rash
    request_payment_method(chat_id)

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
    return {"status": "healthy", "service": "Tokio Sushi Premium Bot", "timestamp": get_uzbekistan_time().isoformat()}

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
                                welcome_text = f"""
🎌 <b>TOKIO SUSHI PREMIUM</b> 🍱

🏮 <b>Добро пожаловать! Премиум японская кухня</b>
⭐ 98 премиум продуктов
🚚 Быстрая доставка
🎁 <b>СКИДКА {DISCOUNT_PERCENT}% НА КАЖДЫЙ ЗАКАЗ!</b>

📞 Связь: +998 91 211 12 15
                                """
                                send_message(chat_id, welcome_text, main_menu(chat_id))
                            
                            elif text == "🍽 Mazali Menyu":
                                show_full_menu(chat_id)
                            
                            elif text == "🛒 Savat":
                                show_cart(chat_id)
                                
                            elif text == "📦 Mening buyurtmalarim":
                                user_orders = [order for order in orders_data.values() if order["user_id"] == chat_id]
                                if user_orders:
                                    text = "📦 <b>ВАШИ ЗАКАЗЫ</b>\n\n"
                                    for order in user_orders[-5:]:
                                        status_emoji = "✅" if order["status"] == "готов" else "⏳" if order["status"] == "принят" else "❌"
                                        text += f"{status_emoji} #{list(orders_data.keys())[list(orders_data.values()).index(order)]} - {order['total_with_delivery']:,} сум - {order['status']}\n"
                                    send_message(chat_id, text)
                                else:
                                    send_message(chat_id, "📦 У вас еще нет заказов")
                            
                            elif text == "ℹ️ Ma'lumot":
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
                            
                            elif text == "👑 Admin Panel" and str(chat_id) == ADMIN_ID:
                                today_orders = len([o for o in orders_data.values() if datetime.fromisoformat(o['timestamp']).date() == get_uzbekistan_time().date()])
                                admin_text = f"""
👑 <b>ПАНЕЛЬ АДМИНИСТРАТОРА</b>

📊 Заказов сегодня: {today_orders} шт
👥 Всего клиентов: {len(user_data)} чел
💰 Всего заказов: {len(orders_data)} шт
🕒 Время: {get_uzbekistan_time().strftime('%H:%M')}
                                """
                                send_message(chat_id, admin_text)
                            
                            elif text == "⬅️ Asosiy menyu" or text == "🏠 Asosiy menyu":
                                send_message(chat_id, "🏠 Главное меню", main_menu(chat_id))
                            
                            # To'lov usullari
                            elif text == "💳 Оплата картой":
                                # Oxirgi buyurtmani topish
                                user_orders = [order_id for order_id, order in orders_data.items() if order["user_id"] == chat_id and order["status"] == "новый"]
                                if user_orders:
                                    last_order_id = max(user_orders)
                                    orders_data[last_order_id]["payment_method"] = "карта"
                                    show_card_payment(chat_id, last_order_id)
                                    send_order_to_admin(last_order_id)
                                else:
                                    send_message(chat_id, "❌ Активный заказ не найден")
                            
                            elif text == "💵 Наличные":
                                # Oxirgi buyurtmani topish
                                user_orders = [order_id for order_id, order in orders_data.items() if order["user_id"] == chat_id and order["status"] == "новый"]
                                if user_orders:
                                    last_order_id = max(user_orders)
                                    orders_data[last_order_id]["payment_method"] = "наличные"
                                    confirm_cash_payment(chat_id, last_order_id)
                                    send_order_to_admin(last_order_id)
                                else:
                                    send_message(chat_id, "❌ Активный заказ не найден")
                            
                            # Telefon qabul qilish
                            elif "contact" in message:
                                contact = message["contact"]
                                phone = contact.get("phone_number", "")
                                
                                if chat_id not in user_data:
                                    user_data[chat_id] = {}
                                user_data[chat_id]["phone"] = phone
                                send_message(chat_id, f"✅ Номер телефона принят: {phone}")
                                
                                # Lokatsiya so'rash
                                request_location(chat_id)
                            
                            # Google Maps lokatsiya qabul qilish
                            elif "location" in message:
                                location = message["location"]
                                lat = location["latitude"]
                                lon = location["longitude"]
                                maps_url = f"https://maps.google.com/?q={lat},{lon}"
                                
                                if chat_id not in user_data:
                                    user_data[chat_id] = {}
                                user_data[chat_id]["location"] = maps_url
                                user_data[chat_id]["location_type"] = "google_maps"
                                send_message(chat_id, f"✅ Адрес принят!\n📍 Google Maps")
                                
                                # Buyurtma yaratish
                                create_order_from_cart(chat_id)
                            
                            # Yandex Maps linkini qabul qilish
                            elif text == "🌐 Отправить Yandex Maps ссылку":
                                send_message(chat_id, "🌐 Пожалуйста, отправьте вашу ссылку Yandex Maps:")
                            
                            # Xarita linklarini qabul qilish
                            elif "maps.google.com" in text or "goo.gl/maps" in text:
                                if chat_id not in user_data:
                                    user_data[chat_id] = {}
                                user_data[chat_id]["location"] = text
                                user_data[chat_id]["location_type"] = "google_maps"
                                send_message(chat_id, f"✅ Адрес Google Maps принят!")
                                
                                # Buyurtma yaratish
                                create_order_from_cart(chat_id)
                            
                            elif "yandex" in text and "maps" in text:
                                if chat_id not in user_data:
                                    user_data[chat_id] = {}
                                user_data[chat_id]["location"] = text
                                user_data[chat_id]["location_type"] = "yandex_maps"
                                send_message(chat_id, f"✅ Адрес Yandex Maps принят!")
                                
                                # Buyurtma yaratish
                                create_order_from_cart(chat_id)
                            
                            # Oddiy matn manzilni qabul qilish
                            elif text and len(text) > 10 and text not in ["🍽 Mazali Menyu", "🛒 Savat", "📦 Mening buyurtmalarim", "ℹ️ Ma'lumot", "👑 Admin Panel", "🏠 Asosiy menyu", "💳 Оплата картой", "💵 Наличные", "📍 Через Google Maps", "🌐 Отправить Yandex Maps ссылку"]:
                                if chat_id not in user_data:
                                    user_data[chat_id] = {}
                                user_data[chat_id]["location"] = text
                                user_data[chat_id]["location_type"] = "text"
                                send_message(chat_id, f"✅ Адрес принят!\n📍 {text}")
                                
                                # Buyurtma yaratish
                                create_order_from_cart(chat_id)
                        
                        elif "callback_query" in update:
                            callback = update["callback_query"]
                            chat_id = callback["message"]["chat"]["id"]
                            callback_data = callback["data"]
                            
                            handle_callback(chat_id, callback_data)
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Ошибка: {e}")
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
