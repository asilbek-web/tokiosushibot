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

# Menyu ma'lumotlari - TO'LIQ YANGILANDI
menu_data = {
    "issiq_taomlar": {
        "name": "🍜 Issiq Taomlar",
        "products": [
            {"id": 1, "name": "Ramen", "price": 55000, "description": "An'anaviy yapon rameni"},
            {"id": 2, "name": "Suyuq Vok", "price": 55000, "description": "Suyuq vok taomi"},
            {"id": 3, "name": "Tom Yam", "price": 95000, "description": "Taylandcha Tom Yam"},
            {"id": 4, "name": "Qanotchalar", "price": 35000, "description": "Qovurilgan tovuq qanotchalar"},
            {"id": 5, "name": "Qarsildoq Baqlajon", "price": 45000, "description": "Qarsildoq baqlajonlar"},
            {"id": 6, "name": "Ramen Maxsus", "price": 66000, "description": "Maxsus ramen"},
            {"id": 7, "name": "Tar-Tar", "price": 95000, "description": "Tar-Tar sousi bilan"},
            {"id": 8, "name": "Mol Go'shtli Vok", "price": 65000, "description": "Mol go'shti bilan vok"},
            {"id": 9, "name": "Kuksi", "price": 40000, "description": "Koreyscha kuksi"},
            {"id": 10, "name": "Tovuqli Sezar", "price": 45000, "description": "Sezar salati"},
            {"id": 11, "name": "Ramen Klassik", "price": 60000, "description": "Klassik ramen"},
            {"id": 12, "name": "Burgjua", "price": 40000, "description": "Burgjua salati"},
            {"id": 13, "name": "Rukola Salati", "price": 50000, "description": "Rukola bilan salat"},
            {"id": 14, "name": "Daryo Salati", "price": 65000, "description": "Baliqli salat"},
            {"id": 15, "name": "Kapriz", "price": 40000, "description": "Kapriz salati"},
            {"id": 16, "name": "Fuka Salati", "price": 35000, "description": "Fuka salati"}
        ]
    },
    "pizza_burger": {
        "name": "🍕 Pizza va Burger",
        "products": [
            {"id": 17, "name": "Klub Sendvich", "price": 35000, "description": "Klub sendvich"},
            {"id": 18, "name": "Tovuq Qanotchalar", "price": 35000, "description": "Qovurilgan tovuq qanotchalar"},
            {"id": 19, "name": "Pishloq Shariklar", "price": 22000, "description": "Pishloq shariklari"},
            {"id": 20, "name": "Fri Kartoshka", "price": 22000, "description": "Qovurilgan kartoshka"},
            {"id": 21, "name": "Chizburger", "price": 33000, "description": "Chizburger"},
            {"id": 22, "name": "Gamburger", "price": 39000, "description": "Gamburger"},
            {"id": 23, "name": "Tokio Burger", "price": 37000, "description": "Tokio maxsus burger"},
            {"id": 24, "name": "Miks Pizza 25sm", "price": 85000, "description": "Aralash pizza 25sm"},
            {"id": 25, "name": "Kuzidirini Pizza 25sm", "price": 80000, "description": "Kuzidirini pizza"},
            {"id": 26, "name": "Margarita Pizza 25sm", "price": 75000, "description": "Margarita pizza"},
            {"id": 27, "name": "Tokio Miks Pizza 32sm", "price": 90000, "description": "Tokio miks pizza 32sm"},
            {"id": 28, "name": "Pishloqli Pizza 32sm", "price": 80000, "description": "Pishloqli pizza"},
            {"id": 29, "name": "Bazi Pizza 32sm", "price": 90000, "description": "Bazi pizza"}
        ]
    },
    "sovuq_rollar": {
        "name": "🍣 Sovuq Rollar",
        "products": [
            {"id": 30, "name": "Filadelfiya Klassik", "price": 80000, "description": "An'anaviy filadelfiya"},
            {"id": 31, "name": "Filadelfiya Gold", "price": 120000, "description": "Eksklyuziv filadelfiya"},
            {"id": 32, "name": "Ebi Gold", "price": 110000, "description": "Krevetka bilan"},
            {"id": 33, "name": "Losos (Gril)", "price": 93000, "description": "Grillangan losos"},
            {"id": 34, "name": "Krabli Kaliforniya", "price": 70000, "description": "Krab bilan kaliforniya"},
            {"id": 35, "name": "Kunjutli Roll", "price": 60000, "description": "Kunjutli roll"},
            {"id": 36, "name": "Qisqichbaqali Kaliforniya", "price": 80000, "description": "Qisqichbaqa bilan"},
            {"id": 37, "name": "Ajdaho Roll", "price": 70000, "description": "Ajdaho roll"},
            {"id": 38, "name": "Lososli Kaliforniya", "price": 76000, "description": "Lososli kaliforniya"},
            {"id": 39, "name": "Kanada Gold", "price": 93000, "description": "Kanada uslubida"},
            {"id": 40, "name": "Tunetsli Filadelfiya", "price": 90000, "description": "Tunets bilan filadelfiya"},
            {"id": 41, "name": "Bodringli Roll", "price": 65000, "description": "Bodringli roll"}
        ]
    },
    "pishirilgan_rollar": {
        "name": "🔥 Pishirilgan Rollar",
        "products": [
            {"id": 42, "name": "Qisqichbaqali Roll", "price": 80000, "description": "Pishirilgan qisqichbaqali"},
            {"id": 43, "name": "Tovuqli Roll", "price": 55000, "description": "Pishirilgan tovuqli"},
            {"id": 44, "name": "Kaliforniya Roll", "price": 70000, "description": "Pishirilgan kaliforniya"},
            {"id": 45, "name": "Lososli Roll", "price": 77000, "description": "Pishirilgan lososli"},
            {"id": 46, "name": "Achchiq Steyk Roll", "price": 99000, "description": "Achchiq steykli"},
            {"id": 47, "name": "Ugorli Roll", "price": 80000, "description": "Pishirilgan ugorli"}
        ]
    },
    "qovurilgan_rollar": {
        "name": "⚡ Qovurilgan Rollar",
        "products": [
            {"id": 48, "name": "Tovuqli Tempura", "price": 48000, "description": "Tovuqli tempura"},
            {"id": 49, "name": "Tunetsli Tempura", "price": 75000, "description": "Tunetsli tempura"},
            {"id": 50, "name": "Ture Tempura", "price": 71000, "description": "Ture tempura"},
            {"id": 51, "name": "Qisqichbaqali Tempura", "price": 70000, "description": "Qisqichbaqali tempura"},
            {"id": 52, "name": "Lososli Tempura", "price": 55000, "description": "Lososli tempura"},
            {"id": 53, "name": "Pishirilgan Tempura", "price": 78000, "description": "Pishirilgan tempura"}
        ]
    },
    "setlar": {
        "name": "🎎 Setlar",
        "products": [
            {"id": 54, "name": "Tokio Set 8шт", "price": 350000, "description": "Tokio seti 8 dona"},
            {"id": 55, "name": "Tokio Set 20шт", "price": 280000, "description": "Tokio seti 20 dona"},
            {"id": 56, "name": "Tokio Set 32шт", "price": 260000, "description": "Tokio seti 32 dona"},
            {"id": 57, "name": "Ideal Set 8шт", "price": 280000, "description": "Ideal set 8 dona"},
            {"id": 58, "name": "Ideal Set 20шт", "price": 260000, "description": "Ideal set 20 dona"},
            {"id": 59, "name": "Ideal Set 32шт", "price": 240000, "description": "Ideal set 32 dona"},
            {"id": 60, "name": "Sakura Set 8шт", "price": 200000, "description": "Sakura set 8 dona"},
            {"id": 61, "name": "Sakura Set 20шт", "price": 180000, "description": "Sakura set 20 dona"},
            {"id": 62, "name": "Sakura Set 32шт", "price": 160000, "description": "Sakura set 32 dona"},
            {"id": 63, "name": "Klassik Set 8шт", "price": 150000, "description": "Klassik set 8 dona"},
            {"id": 64, "name": "Klassik Set 20шт", "price": 130000, "description": "Klassik set 20 dona"},
            {"id": 65, "name": "Klassik Set 32шт", "price": 120000, "description": "Klassik set 32 dona"},
            {"id": 66, "name": "Okay Set 8шт", "price": 220000, "description": "Okay set 8 dona"},
            {"id": 67, "name": "Okay Set 20шт", "price": 200000, "description": "Okay set 20 dona"},
            {"id": 68, "name": "Okay Set 32шт", "price": 180000, "description": "Okay set 32 dona"},
            {"id": 69, "name": "Yamomoto Set 8шт", "price": 250000, "description": "Yamomoto set 8 dona"},
            {"id": 70, "name": "Yamomoto Set 20шт", "price": 230000, "description": "Yamomoto set 20 dona"},
            {"id": 71, "name": "Yamomoto Set 32шт", "price": 210000, "description": "Yamomoto set 32 dona"}
        ]
    },
    "sushi_gunkan": {
        "name": "🍱 Sushi va Gunkan",
        "products": [
            {"id": 72, "name": "Mini Losos", "price": 24000, "description": "Mini losos sushi"},
            {"id": 73, "name": "Mini Ugor", "price": 24000, "description": "Mini ugor sushi"},
            {"id": 74, "name": "Mini Bodring", "price": 15000, "description": "Mini bodring sushi"},
            {"id": 75, "name": "Mini Tunets", "price": 24000, "description": "Mini tunets sushi"},
            {"id": 76, "name": "Mini Krab", "price": 24000, "description": "Mini krab sushi"},
            {"id": 77, "name": "Lososli Sushi", "price": 25000, "description": "Lososli sushi"},
            {"id": 78, "name": "Tunetsli Sushi", "price": 25000, "description": "Tunetsli sushi"},
            {"id": 79, "name": "Qisqichbaqali Sushi", "price": 20000, "description": "Qisqichbaqali sushi"},
            {"id": 80, "name": "Massago Gunkan", "price": 24000, "description": "Massago gunkan"},
            {"id": 81, "name": "Tunetsli Gunkan", "price": 30000, "description": "Tunetsli gunkan"},
            {"id": 82, "name": "Lososli Gunkan", "price": 24000, "description": "Lososli gunkan"},
            {"id": 83, "name": "Ugorli Gunkan", "price": 23000, "description": "Ugorli gunkan"}
        ]
    },
    "ichimliklar": {
        "name": "🥤 Ichimliklar",
        "products": [
            {"id": 84, "name": "Qulupnayli Milkshake", "price": 30000, "description": "Qulupnayli milkshake"},
            {"id": 85, "name": "Oreo Milkshake", "price": 30000, "description": "Oreo milkshake"},
            {"id": 86, "name": "Kinder Milkshake", "price": 30000, "description": "Kinder milkshake"},
            {"id": 87, "name": "Snickers Milkshake", "price": 30000, "description": "Snickers milkshake"},
            {"id": 88, "name": "Bananli Milkshake", "price": 30000, "description": "Bananli milkshake"},
            {"id": 89, "name": "Mo'jizaviy Choy", "price": 35000, "description": "Maxsus choy"},
            {"id": 90, "name": "Tokio Choyi", "price": 35000, "description": "Tokio maxsus choy"},
            {"id": 91, "name": "Mevali Choy", "price": 35000, "description": "Mevali choy"},
            {"id": 92, "name": "Tarxun Choyi", "price": 35000, "description": "Tarxun choyi"},
            {"id": 93, "name": "Rayhon Choyi", "price": 35000, "description": "Rayhon choyi"},
            {"id": 94, "name": "Karkade Choyi", "price": 30000, "description": "Karkade choyi"},
            {"id": 95, "name": "Limonli Choy", "price": 25000, "description": "Limonli choy"},
            {"id": 96, "name": "Sok", "price": 19000, "description": "Tabiiy sok"},
            {"id": 97, "name": "Kola/Fanta/Sprite 1L", "price": 14000, "description": "Gazlangan ichimlik 1L"},
            {"id": 98, "name": "Kola 0.5L", "price": 9000, "description": "Kola 0.5L"},
            {"id": 99, "name": "Gazsiz Suv", "price": 8000, "description": "Gazsiz suv"},
            {"id": 100, "name": "Moxito 1L", "price": 45000, "description": "Moxito 1L"},
            {"id": 101, "name": "Moxito 0.7L", "price": 25000, "description": "Moxito 0.7L"},
            {"id": 102, "name": "Moxito 0.5L", "price": 20000, "description": "Moxito 0.5L"},
            {"id": 103, "name": "Gonkong Mevali Kofe", "price": 20000, "description": "Gonkong mevali kofe"},
            {"id": 104, "name": "Gonkong Kalnali Kofe", "price": 20000, "description": "Gonkong kalnali kofe"},
            {"id": 105, "name": "Gonkong Vanil Kofe", "price": 20000, "description": "Gonkong vanil kofe"},
            {"id": 106, "name": "Gonkong Kofe", "price": 20000, "description": "Gonkong kofe"}
        ]
    },
    "shirinliklar": {
        "name": "🍰 Shirinliklar",
        "products": [
            {"id": 107, "name": "Tiramisu", "price": 30000, "description": "Italiyaning tiramisu deserti"},
            {"id": 108, "name": "Klassik Chizkeyk", "price": 45000, "description": "Klassik chizkeyk"},
            {"id": 109, "name": "Blinchiklar", "price": 20000, "description": "Shirin blinchiklar"},
            {"id": 110, "name": "Kanada Desert", "price": 20000, "description": "Kanada uslubida desert"},
            {"id": 111, "name": "Qulupnay Desert", "price": 20000, "description": "Qulupnayli desert"}
        ]
    }
}

# Foydalanuvchilar ma'lumoti
user_data = {}
# Buyurtmalar ma'lumoti
orders_data = {}

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

def main_menu():
    keyboard = {
        "keyboard": [
            ["🍜 Menyu", "📥 Savat"],
            ["📦 Mening buyurtmalarim", "ℹ️ Ma'lumot"],
            ["👑 Admin Panel"]
        ],
        "resize_keyboard": True
    }
    return keyboard

def show_menu(chat_id):
    keyboard = {
        "keyboard": [
            ["🍜 Issiq Taomlar", "🍕 Pizza va Burger"],
            ["🍣 Sovuq Rollar", "🔥 Pishirilgan Rollar"],
            ["⚡ Qovurilgan Rollar", "🎎 Setlar"],
            ["🍱 Sushi va Gunkan", "🥤 Ichimliklar"],
            ["🍰 Shirinliklar", "⬅️ Orqaga"]
        ],
        "resize_keyboard": True
    }
    
    text = """
🍱 <b>TOKIO SUSHI MENYU</b> 🎌

🏮 Marhamat, kerakli bo'limni tanlang:
⭐ Bizda 111 ta mahsulot mavjud
🚚 Yetkazib berish: 30-45 daqiqa
💰 Yetkazish: TEKIN
    """
    send_message(chat_id, text, keyboard)

def show_category_products(chat_id, category_key):
    if category_key not in menu_data:
        send_message(chat_id, "❌ Kategoriya topilmadi")
        return
    
    category = menu_data[category_key]
    products = category["products"]
    
    text = f"🍱 <b>{category['name']}</b>\n\n"
    
    # Mahsulotlarni guruhlab ko'rsatish (6 tadan)
    for i in range(0, len(products), 6):
        product_group = products[i:i+6]
        
        # Har bir mahsulot uchun inline keyboard yaratish
        keyboard = {"inline_keyboard": []}
        
        for product in product_group:
            keyboard["inline_keyboard"].append([
                {
                    "text": f"{product['name']} - {product['price']:,} so'm",
                    "callback_data": f"add_{product['id']}"
                }
            ])
        
        # Bo'limlararo navigatsiya
        if len(products) > 6:
            nav_buttons = []
            if i > 0:
                nav_buttons.append({"text": "⬅️ Oldingi", "callback_data": f"page_{category_key}_{i-6}"})
            if i + 6 < len(products):
                nav_buttons.append({"text": "Keyingi ➡️", "callback_data": f"page_{category_key}_{i+6}"})
            if nav_buttons:
                keyboard["inline_keyboard"].append(nav_buttons)
        
        keyboard["inline_keyboard"].append([{"text": "📥 Savatga qo'shish", "callback_data": "view_cart"}])
        keyboard["inline_keyboard"].append([{"text": "⬅️ Orqaga", "callback_data": "back_to_menu"}])
        
        group_text = text
        for product in product_group:
            group_text += f"🍣 {product['name']} - {product['price']:,} so'm\n"
            group_text += f"   {product['description']}\n\n"
        
        send_message(chat_id, group_text, keyboard)
        break  # Faqat birinchi guruhni ko'rsatish

def handle_callback(chat_id, callback_data):
    if callback_data.startswith("add_"):
        product_id = int(callback_data.split("_")[1])
        add_to_cart(chat_id, product_id)
    elif callback_data == "view_cart":
        show_cart(chat_id)
    elif callback_data == "back_to_menu":
        show_menu(chat_id)
    elif callback_data.startswith("page_"):
        parts = callback_data.split("_")
        category_key = parts[1]
        start_index = int(parts[2])
        show_category_page(chat_id, category_key, start_index)

def add_to_cart(chat_id, product_id):
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
📝 {product['description']}

🛒 Savatingizdagi mahsulotlar: {len(user_data[chat_id]['cart'])} ta
    """
    send_message(chat_id, text)

def show_cart(chat_id):
    if chat_id not in user_data or "cart" not in user_data[chat_id] or not user_data[chat_id]["cart"]:
        send_message(chat_id, "🛒 Savatingiz bo'sh")
        return
    
    cart = user_data[chat_id]["cart"]
    total = sum(item['price'] for item in cart)
    
    text = "🛒 <b>SAVATINGIZ</b>\n\n"
    for i, item in enumerate(cart, 1):
        text += f"{i}. {item['name']} - {item['price']:,} so'm\n"
    
    text += f"\n💰 <b>Jami: {total:,} so'm</b>"
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "✅ Buyurtma berish", "callback_data": "place_order"}],
            [{"text": "🗑 Savatni tozalash", "callback_data": "clear_cart"}],
            [{"text": "⬅️ Orqaga", "callback_data": "back_to_menu"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def place_order(chat_id):
    if chat_id not in user_data or "cart" not in user_data[chat_id] or not user_data[chat_id]["cart"]:
        send_message(chat_id, "❌ Savatingiz bo'sh")
        return
    
    cart = user_data[chat_id]["cart"]
    total = sum(item['price'] for item in cart)
    order_id = len(orders_data) + 1
    
    # Buyurtmani saqlash
    orders_data[order_id] = {
        "user_id": chat_id,
        "items": cart.copy(),
        "total": total,
        "status": "yangi",
        "timestamp": datetime.now().isoformat()
    }
    
    # Savatni tozalash
    user_data[chat_id]["cart"] = []
    
    # Foydalanuvchiga xabar
    text = f"""
✅ <b>BUYURTMA QABUL QILINDI</b>

📦 Buyurtma raqami: #{order_id}
💰 Jami summa: {total:,} so'm
⏰ Yetkazib berish: 30-45 daqiqa
🚚 Yetkazish: TEKIN

📞 Bog'lanish: +998947126030
    """
    send_message(chat_id, text, main_menu())
    
    # Adminga xabar
    admin_text = f"""
🆕 <b>YANGI BUYURTMA</b>

👤 Foydalanuvchi: {chat_id}
📦 Buyurtma raqami: #{order_id}
💰 Summa: {total:,} so'm
⏰ Vaqt: {datetime.now().strftime('%H:%M')}

📦 Mahsulotlar:
"""
    for item in cart:
        admin_text += f"• {item['name']} - {item['price']:,} so'm\n"
    
    send_message(ADMIN_ID, admin_text)

def admin_panel(chat_id):
    if str(chat_id) != ADMIN_ID:
        send_message(chat_id, "❌ Sizda admin huquqi yo'q")
        return
    
    keyboard = {
        "keyboard": [
            ["📊 Bugun statistikasi", "📈 Haftalik statistika"],
            ["📦 Faol buyurtmalar", "✅ Bajarilgan buyurtmalar"],
            ["👥 Foydalanuvchilar", "💰 Daromad"],
            ["📢 Reklama yuborish", "⚙️ Sozlamalar"],
            ["⬅️ Foydalanuvchi rejimi"]
        ],
        "resize_keyboard": True
    }
    
    text = """
👑 <b>ADMIN PANEL</b> 🎌

🏮 Tokio Sushi Boshqaruvi
📊 Botning to'liq boshqaruvi
    """
    send_message(chat_id, text, keyboard)

def show_today_stats(chat_id):
    today = datetime.now().date()
    today_orders = [order for order in orders_data.values() 
                   if datetime.fromisoformat(order['timestamp']).date() == today]
    
    total_orders = len(today_orders)
    total_revenue = sum(order['total'] for order in today_orders)
    
    text = f"""
📊 <b>BUGUNGI STATISTIKA</b>

🕒 Sana: {today.strftime('%Y-%m-%d')}
📦 Buyurtmalar: {total_orders} ta
💰 Daromad: {total_revenue:,} so'm
👥 Faol foydalanuvchilar: {len(user_data)} ta
⭐ O'rtacha buyurtma: {total_revenue//total_orders if total_orders > 0 else 0:,} so'm
    """
    send_message(chat_id, text)

def cancel_order(chat_id):
    if chat_id in user_data and user_data[chat_id].get("cart"):
        user_data[chat_id]["cart"] = []
        send_message(chat_id, "❌ Buyurtma bekor qilindi. Savatchangiz tozalandi.", main_menu())
        
        # Adminga xabar
        admin_msg = f"⚠️ Buyurtma bekor qilindi:\n👤 Foydalanuvchi: {chat_id}\n⏰ Vaqt: {datetime.now().strftime('%H:%M')}"
        send_message(ADMIN_ID, admin_msg)
    else:
        send_message(chat_id, "❌ Bekor qilish uchun faol buyurtma topilmadi.")

def order_status(chat_id):
    text = """
⏳ <b>BUYURTMA HOLATI</b>

📦 Buyurtmangiz qabul qilindi va tayyorlanmoqda
⏰ Taxminiy tayyor bo'lish vaqti: 30-45 daqiqa
🚚 Yetkazib berish: TEKIN

📞 Agar savollaringiz bo'lsa: +998947126030
    """
    send_message(chat_id, text, main_menu())

def show_category_page(chat_id, category_key, start_index):
    if category_key not in menu_data:
        send_message(chat_id, "❌ Kategoriya topilmadi")
        return
    
    category = menu_data[category_key]
    products = category["products"]
    
    if start_index >= len(products):
        start_index = 0
    
    text = f"🍱 <b>{category['name']}</b>\n\n"
    current_products = products[start_index:start_index+6]
    
    for product in current_products:
        text += f"🍣 {product['name']} - {product['price']:,} so'm\n"
        text += f"   {product['description']}\n\n"
    
    keyboard = {"inline_keyboard": []}
    
    for product in current_products:
        keyboard["inline_keyboard"].append([
            {
                "text": f"{product['name']} - {product['price']:,} so'm",
                "callback_data": f"add_{product['id']}"
            }
        ])
    
    # Navigatsiya tugmalari
    nav_buttons = []
    if start_index > 0:
        nav_buttons.append({"text": "⬅️ Oldingi", "callback_data": f"page_{category_key}_{max(0, start_index-6)}"})
    if start_index + 6 < len(products):
        nav_buttons.append({"text": "Keyingi ➡️", "callback_data": f"page_{category_key}_{start_index+6}"})
    
    if nav_buttons:
        keyboard["inline_keyboard"].append(nav_buttons)
    
    keyboard["inline_keyboard"].append([{"text": "📥 Savatga qo'shish", "callback_data": "view_cart"}])
    keyboard["inline_keyboard"].append([{"text": "⬅️ Orqaga", "callback_data": "back_to_menu"}])
    
    send_message(chat_id, text, keyboard)

def run_bot():
    print("🚀 Tokio Sushi Pro Bot ishga tushdi!")
    print(f"👑 Admin: {ADMIN_ID}")
    print("📞 Support: +998947126030")
    print("⏰ Yetkazish: 30-45 daqiqa")
    print("🍣 Mahsulotlar: 111 ta")
    
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
                            text = message_data.get("text", "")
                            
                            # Start command
                            if text == "/start":
                                welcome_text = """
🍱 <b>TOKIO SUSHI</b> 🎌

🏮 Xush kelibsiz! Tokio Sushi'ning rasmiy botiga.
⭐ Sifatli yapon oshxonasi
🚚 Tezkor yetkazib berish: 30-45 daqiqa
💰 Yetkazish: TEKIN

📞 Bog'lanish: +998947126030
                                """
                                send_message(chat_id, welcome_text, main_menu())
                            
                            # Asosiy menyu
                            elif text == "🍜 Menyu":
                                show_menu(chat_id)
                            
                            # Kategoriyalar
                            elif text in ["🍜 Issiq Taomlar", "🍕 Pizza va Burger", "🍣 Sovuq Rollar", 
                                        "🔥 Pishirilgan Rollar", "⚡ Qovurilgan Rollar", "🎎 Setlar",
                                        "🍱 Sushi va Gunkan", "🥤 Ichimliklar", "🍰 Shirinliklar"]:
                                category_map = {
                                    "🍜 Issiq Taomlar": "issiq_taomlar",
                                    "🍕 Pizza va Burger": "pizza_burger", 
                                    "🍣 Sovuq Rollar": "sovuq_rollar",
                                    "🔥 Pishirilgan Rollar": "pishirilgan_rollar",
                                    "⚡ Qovurilgan Rollar": "qovurilgan_rollar",
                                    "🎎 Setlar": "setlar",
                                    "🍱 Sushi va Gunkan": "sushi_gunkan",
                                    "🥤 Ichimliklar": "ichimliklar",
                                    "🍰 Shirinliklar": "shirinliklar"
                                }
                                show_category_products(chat_id, category_map[text])
                            
                            elif text == "📥 Savat":
                                show_cart(chat_id)
                            
                            elif text == "📦 Mening buyurtmalarim":
                                order_status(chat_id)
                            
                            elif text == "ℹ️ Ma'lumot":
                                info_text = """
🏮 <b>TOKIO SUSHI</b> 🎌

⭐ Sifatli yapon oshxonasi
🕒 Ish vaqti: 10:00 - 23:00
🚚 Yetkazib berish: 30-45 daqiqa
💰 Yetkazish: TEKIN

📞 Bog'lanish: +998947126030
📍 Manzil: Toshkent shahar
                                """
                                send_message(chat_id, info_text, main_menu())
                            
                            elif text == "👑 Admin Panel" and str(chat_id) == ADMIN_ID:
                                admin_panel(chat_id)
                            
                            elif text == "📊 Bugun statistikasi" and str(chat_id) == ADMIN_ID:
                                show_today_stats(chat_id)
                            
                            elif text == "❌ Bekor qilish":
                                cancel_order(chat_id)
                            
                            elif text == "📦 Buyurtma holati":
                                order_status(chat_id)
                            
                            elif text == "⬅️ Orqaga":
                                send_message(chat_id, "🏠 Asosiy menyu", main_menu())
                            
                            elif text == "⬅️ Foydalanuvchi rejimi" and str(chat_id) == ADMIN_ID:
                                send_message(chat_id, "👤 Foydalanuvchi rejimiga o'tildi", main_menu())
                        
                        elif "callback_query" in update:
                            callback = update["callback_query"]
                            chat_id = callback["message"]["chat"]["id"]
                            callback_data = callback["data"]
                            
                            if callback_data == "place_order":
                                place_order(chat_id)
                            elif callback_data == "clear_cart":
                                if chat_id in user_data:
                                    user_data[chat_id]["cart"] = []
                                send_message(chat_id, "🗑 Savat tozalandi")
                            else:
                                handle_callback(chat_id, callback_data)
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Xato: {e}")
            time.sleep(3)

@app.route('/')
def home():
    return "🍱 Tokio Sushi Bot ishlamoqda!"

if __name__ == "__main__":
    bot_thread = Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
