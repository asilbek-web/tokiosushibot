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

# Tillar
LANGUAGES = {
    "uz": "O'zbekcha",
    "ru": "Русский"
}

user_language = {}
user_data = {}
orders_data = {}
user_feedback = {}
order_counter = 1

# TO'LIQ MENYU MA'LUMOTLARI - RUS TILIDA
menu_data = {
    "holodnye_rolly": {
        "name": "🍣 ХОЛОДНЫЕ РОЛЛЫ",
        "emoji": "🍣",
        "products": [
            {"id": 1, "name": "Филадельфия Голд", "price": 120000, "description": "Сыр.Лосось.Огурец.Угорь.Унаги соус.Тунец.Кунжут.Массаго икра", "prep_time": "20 daqiqa", "image_url": "https://ibb.co/MxFj5fc9", "composition": ["Гурч", "Лосось", "Моццарелла сыр", "Майонез"]},
            {"id": 2, "name": "Филадельфия (Тунец)", "price": 90000, "description": "Сыр.Тунец", "prep_time": "15 daqiqa", "image_url": "https://ibb.co/ymzTLB2d", "composition": ["Гурч", "Тунец", "Моццарелла сыр"]},
            {"id": 3, "name": "Филадельфия Классик", "price": 80000, "description": "Сыр.Огурецы.Лосось", "prep_time": "12 daqiqa", "image_url": "https://ibb.co/gLGNmQNL", "composition": ["Гурч", "Лосось", "Огурец", "Моццарелла сыр"]},
            {"id": 4, "name": "Эби Голд", "price": 110000, "description": "Сыр.Лосось.Креветки в кляре.Огурец.Лук", "prep_time": "18 daqiqa", "image_url": "https://ibb.co/TBMTxXkK", "composition": ["Гурч", "Лосось", "Креветки", "Огурец", "Лук"]},
            {"id": 5, "name": "Лосось (гриль)", "price": 93000, "description": "Сыр.Унаги соус.Лосось.Массаго", "prep_time": "15 daqiqa", "image_url": "https://ibb.co/Q7tpSZRW", "composition": ["Гурч", "Лосось гриль", "Унаги соус", "Массаго"]},
            {"id": 6, "name": "Калифорния с креветками", "price": 80000, "description": "Сыр.Огурец.Креветки тигровые.Массаго красс", "prep_time": "12 daqiqa", "image_url": "https://ibb.co/LzWDsSLL", "composition": ["Гурч", "Креветки", "Огурец", "Массаго"]},
            {"id": 7, "name": "Калифорния с лососем", "price": 76000, "description": "Сыр.Огурец.Лосось.Массаго красс", "prep_time": "12 daqiqa", "image_url": "https://ibb.co/x8mtrwnr", "composition": ["Гурч", "Лосось", "Огурец", "Массаго"]},
            {"id": 8, "name": "Калифорния с крабом", "price": 70000, "description": "Сыр.Огурец.Снежный краб.Массаго красный", "prep_time": "12 daqiqa", "image_url": "https://ibb.co/GQC6b0Jx", "composition": ["Гурч", "Краб", "Огурец", "Массаго"]},
            {"id": 9, "name": "Ролл Огурец", "price": 65000, "description": "Сыр.Стружка тунца.Огурец", "prep_time": "10 daqiqa", "image_url": "https://ibb.co/qMwVCNkJ", "composition": ["Гурч", "Огурец", "Стружка тунца"]},
            {"id": 91, "name": "Ролл в Кунжуте", "price": 50000, "description": "Сыр.Кунжут.Краб", "prep_time": "15 daqiqa", "image_url": "https://ibb.co/npfwvNQ", "composition": ["Гурч", "Кунжут", "Краб"]},
            {"id": 92, "name": "Дракон", "price": 75000, "description": "Сыр.Угорь.Огурец", "prep_time": "15 daqiqa", "image_url": "https://ibb.co/cXNm1Lws", "composition": ["Гурч", "Угорь", "Огурец"]},
            {"id": 93, "name": "Канада GOLD", "price": 85000, "description": "Сыр.Лосось.Огурец.Угорь.Унаги соус.Кунжут", "prep_time": "20 daqiqa", "image_url": "https://ibb.co/ZRX11xwV", "composition": ["Гурч", "Лосось", "Огурец", "Угорь", "Унаги соус"]}
        ]
    },
    "zapechennye": {
        "name": "🔥 ЗАПЕЧЕННЫЕ ФИРМЕННЫЕ РОЛЛЫ ОТ:",
        "emoji": "🔥",
        "products": [
            {"id": 10, "name": "Ролл Филадельфия Стейк", "price": 95000, "description": "Сыр.лосось.огурец.сырная шапка", "prep_time": "18 daqiqa", "image_url": "https://ibb.co/V03yy7Jy", "composition": ["Гурч", "Лосось", "Огурец", "Сырная шапка"]},
            {"id": 11, "name": "Ролл с креветкой", "price": 80000, "description": "Сыр.Тигровые креветки.сырная шапка.Огурец.кунжут", "prep_time": "16 daqiqa", "image_url": "https://ibb.co/zWPhtZ2m", "composition": ["Гурч", "Креветки", "Сырная шапка", "Огурец"]},
            {"id": 12, "name": "Ролл с угрем", "price": 80000, "description": "Сыр.огурецы.кунжут.сырная шапка.угорь", "prep_time": "16 daqiqa", "image_url": "https://ibb.co/C5qhrcSR", "composition": ["Гурч", "Угорь", "Сырная шапка", "Огурец"]},
            {"id": 13, "name": "Ролл с крабом", "price": 66000, "description": "Сыр.Огурец.Снежный краб", "prep_time": "14 daqiqa", "image_url": "https://ibb.co/VZkcJx2", "composition": ["Гурч", "Краб", "Огурец"]},
            {"id": 14, "name": "Ролл с лососем", "price": 77000, "description": "Сыр.Огурецы.кунжут,сырная шапка,лосось,унаги соус", "prep_time": "15 daqiqa", "image_url": "https://ibb.co/TD83xGMz", "composition": ["Гурч", "Лосось", "Сырная шапка", "Огурец"]},
            {"id": 15, "name": "Ролл Калифорния", "price": 70000, "description": "Сыр.Огурецы.снежный краб.икра массаго.сырная шапка.унаги соус", "prep_time": "14 daqiqa", "image_url": "https://ibb.co/Zzn5hb1c", "composition": ["Гурч", "Краб", "Сырная шапка", "Огурец"]},
            {"id": 16, "name": "Ролл с курицей", "price": 55000, "description": "Майонез.Салат Айзберг.курица.сырная шапка", "prep_time": "12 daqiqa", "image_url": "https://ibb.co/XfGFW7Ss", "composition": ["Гурч", "Курица", "Сырная шапка", "Салат Айзберг"]},
            {"id": 94, "name": "ТЕМПУРА c Лосось", "price": 66000, "description": "Лосось, Кунжут", "prep_time": "15 daqiqa", "image_url": "https://ibb.co/MxzTgnLD", "composition": ["Гурч", "Лосось", "Кунжут"]},
            {"id": 95, "name": "Темпура с крабом", "price": 55000, "description": "Краб.Мойонез.Унаги соус", "prep_time": "15 daqiqa", "image_url": "https://ibb.co/bj64nKKm", "composition": ["Гурч", "Краб", "Унаги соус"]},
            {"id": 96, "name": "ТЕМПУРА Креветки", "price": 70000, "description": "Креветки, сырная шапка", "prep_time": "15 daqiqa", "image_url": "https://ibb.co/1JRBHPQj", "composition": ["Гурч", "Креветки", "Сырная шапка"]},
            {"id": 97, "name": "Темпура запеченный", "price": 70000, "description": "Сыр.Краб.Огурец", "prep_time": "15 daqiqa", "image_url": "https://ibb.co/CKC4dXxm", "composition": ["Гурч", "Краб", "Огурец"]}
        ]
    },
    "jarennye_rolly": {
        "name": "⚡ ЖАРЕНЫЕ РОЛЛЫ",
        "emoji": "⚡",
        "products": [
            {"id": 17, "name": "Темпура (Тунец)", "price": 75000, "description": "Огурец.Сыр.Тунец", "prep_time": "15 daqiqa", "image_url": "https://ibb.co/QFjbcnG9", "composition": ["Гурч", "Тунец", "Огурец"]},
            {"id": 18, "name": "Темпура Угорь", "price": 71000, "description": "Сыр.Огурец.Угорь.Массаго красс.Унаги соус", "prep_time": "15 daqiqa", "image_url": "https://ibb.co/d4QM7zfJ", "composition": ["Гурч", "Угорь", "Огурец", "Унаги соус"]},
            {"id": 19, "name": "Темпура с креветками", "price": 70000, "description": "Сыр.Огурец.Креветки тигровые.Массаго красс.Унаги соус", "prep_time": "15 daqiqa", "image_url": "https://ibb.co/1JRBHPQj", "composition": ["Гурч", "Креветки", "Огурец", "Унаги соус"]},
            {"id": 20, "name": "Темпура с лососем", "price": 66000, "description": "Сыр.Огурец.Лосось.Унаги соус.Кунжут", "prep_time": "14 daqiqa", "image_url": "https://ibb.co/MxzTgnLD", "composition": ["Гурч", "Лосось", "Огурец", "Унаги соус"]},
            {"id": 21, "name": "Темпура Курица", "price": 48000, "description": "Айсберг.Майонез.Курица.Унаги соус", "prep_time": "12 daqiqa", "image_url": "https://ibb.co/qQJVGwz", "composition": ["Гурч", "Курица", "Салат Айсберг", "Унаги соус"]},
        ]
    },
    "sety": {
        "name": "🎎 СЕТЛАР",
        "emoji": "🎎",
        "products": [
            {"id": 22, "name": "Сет Токио 48шт", "price": 390000, "description": "Дракон ролл 8шт + Филадельфия классик 8шт + Темпура Лосось 8шт + Краб Запеченый 16шт + Калифорния Лосось 8шт", "prep_time": "40 daqiqa", "image_url": "https://ibb.co/3ycXwTn3", "composition": ["Дракон ролл", "Филадельфия классик", "Темпура Лосось", "Краб Запеченый", "Калифорния Лосось"]},
            {"id": 23, "name": "Сет Ямамото 32шт", "price": 290000, "description": "Филадельфия классик 8шт + Калифорния классик 8шт + Ролл с креветками 8шт + Ролл Чука 8шт", "prep_time": "35 daqiqa", "image_url": "https://ibb.co/DHsDJyTf", "composition": ["Филадельфия классик", "Калифорния классик", "Ролл с креветками", "Ролл Чука"]},
            {"id": 24, "name": "Сет Идеал 32шт", "price": 260000, "description": "Филадельфия классик 8шт + Калифорния Кунсут 8шт + Калифорния Черный 8шт + Дракон ролл 8шт", "prep_time": "32 daqiqa", "image_url": "https://ibb.co/bMnZDM8v", "composition": ["Филадельфия классик", "Калифорния Кунсут", "Калифорния Черный", "Дракон ролл"]},
            {"id": 25, "name": "Сет Окей 24шт", "price": 200000, "description": "Филадельфия классик 8шт + Запеченый лосось 8шт + Темпура лосось 8шт", "prep_time": "30 daqiqa", "image_url": "https://ibb.co/YFfW3pFJ", "composition": ["Филадельфия классик", "Запеченый лосось", "Темпура лосось"]},
            {"id": 26, "name": "Сет Сакура 24шт", "price": 180000, "description": "Филадельфия классик 4шт + Канада Голд 4шт + Мини ролл лосось 8шт + Темпура лосось 8шт", "prep_time": "28 daqiqa", "image_url": "https://ibb.co/FLrCy969", "composition": ["Филадельфия классик", "Канада Голд", "Мини ролл лосось", "Темпура лосось"]},
            {"id": 27, "name": "Сет Классический 32шт", "price": 150000, "description": "Мини ролл лосось 8шт + Мини ролл огурец 8шт + Мини ролл тунец 8шт + Мини ролл краб 8шт", "prep_time": "25 daqiqa", "image_url": "https://ibb.co/Q3B6yMxV", "composition": ["Мини ролл лосось", "Мини ролл огурец", "Мини ролл тунец", "Мини ролл краб"]}
        ]
    },
    "sushi_gunkan": {
        "name": "🍱 СУШИ ВА ГУНКАН",
        "emoji": "🍱",
        "products": [
            {"id": 28, "name": "Гункан Тунец", "price": 30000, "description": "Tunetsli gunkan", "prep_time": "5 daqiqa", "image_url": "https://ibb.co/dNZyGMn", "composition": ["Гурч", "Тунец"]},
            {"id": 29, "name": "Суши Тунец", "price": 25000, "description": "Tunetsli sushi", "prep_time": "5 daqiqa", "image_url": "https://ibb.co/VpSTV2jZ", "composition": ["Гурч", "Тунец"]},
            {"id": 30, "name": "Мини Тунец", "price": 34000, "description": "Mini tunets sushi", "prep_time": "5 daqiqa", "image_url": "https://ibb.co/8Dkf54z0", "composition": ["Гурч", "Тунец"]},
            {"id": 31, "name": "Гункан Лосось", "price": 24000, "description": "Lososli gunkan", "prep_time": "5 daqiqa", "image_url": "https://ibb.co/gZpQSSzf", "composition": ["Гурч", "Лосось"]},
            {"id": 32, "name": "Суши Лосось", "price": 20000, "description": "Lososli sushi", "prep_time": "5 daqiqa", "image_url": "https://ibb.co/JWYVRq3Z", "composition": ["Гурч", "Лосось"]},
            {"id": 33, "name": "Мини Лосось", "price": 34000, "description": "Mini losos sushi", "prep_time": "5 daqiqa", "image_url": "https://ibb.co/DfnTqrM8", "composition": ["Гурч", "Лосось"]},
            {"id": 34, "name": "Гункан Угорь", "price": 24000, "description": "Ugorli gunkan", "prep_time": "5 daqiqa", "image_url": "https://ibb.co/sdBH78W4", "composition": ["Гурч", "Угорь"]},
            {"id": 35, "name": "Суши Угорь", "price": 23000, "description": "Ugorli sushi", "prep_time": "5 daqiqa", "image_url": "https://ibb.co/yck5fm10", "composition": ["Гурч", "Угорь"]},
            {"id": 36, "name": "Мини Угорь", "price": 34000, "description": "Mini ugor sushi", "prep_time": "5 daqiqa", "image_url": "https://ibb.co/mF8yM6TC", "composition": ["Гурч", "Угорь"]},
            {"id": 37, "name": "Гункан Массаго", "price": 24000, "description": "Massago gunkan", "prep_time": "5 daqiqa", "image_url": "https://ibb.co/fVjKB1vS", "composition": ["Гурч", "Массаго"]},
            {"id": 38, "name": "Суши Креветка", "price": 20000, "description": "Qisqichbaqali sushi", "prep_time": "5 daqiqa", "image_url": "https://ibb.co/wZ8cHQ3B", "composition": ["Гурч", "Креветка"]},
            {"id": 39, "name": "Мини Краб", "price": 23000, "description": "Mini krab sushi", "prep_time": "5 daqiqa", "image_url": "https://ibb.co/DPpPLQgg", "composition": ["Гурч", "Краб"]},
            {"id": 40, "name": "Мини Огурец", "price": 15000, "description": "Mini bodring sushi", "prep_time": "5 daqiqa", "image_url": "https://ibb.co/JWN5qYyb", "composition": ["Гурч", "Огурец"]}
        ]
    },
    "goryachaya_eda": {
        "name": "🍜 ГОРЯЧАЯ ЕДА",
        "emoji": "🍜",
        "products": [
            {"id": 41, "name": "Рамэн Классик", "price": 80000, "description": "An'anaviy yapon rameni", "prep_time": "20 daqiqa", "image_url": "https://ibb.co/57sXdTZ", "composition": ["Лапша", "Бульон", "Яйцо", "Свинина"]},
            {"id": 42, "name": "Рамэн Токио", "price": 66000, "description": "Maxsus ramen", "prep_time": "25 daqiqa", "image_url": "https://ibb.co/k20FYLZs", "composition": ["Лапша", "Бульон", "Яйцо", "Свинина", "Овощи"]},
            {"id": 43, "name": "Вок с говядиной", "price": 65000, "description": "Mol go'shti bilan vok", "prep_time": "15 daqiqa", "image_url": "https://ibb.co/4nrmxLW2", "composition": ["Говядина", "Овощи", "Соус"]},
            {"id": 44, "name": "Том Ям Токио", "price": 95000, "description": "Taylandcha Tom Yam", "prep_time": "30 daqiqa", "image_url": "https://ibb.co/Xx1ghHBw", "composition": ["Креветки", "Грибы", "Кокосовое молоко", "Пряности"]},
            {"id": 47, "name": "Вок с курицей", "price": 55000, "description": "Tovuqli vok", "prep_time": "12 daqiqa", "image_url": "https://ibb.co/p6SdB15J", "composition": ["Курица", "Овощи", "Соус"]},
            {"id": 48, "name": "Том Ям Классик", "price": 70000, "description": "Oddiy Tom Yam", "prep_time": "25 daqiqa", "image_url": "https://ibb.co/rfbG3L2h", "composition": ["Креветки", "Грибы", "Лемонграсс"]},
            {"id": 49, "name": "Хрустящие баклажаны", "price": 45000, "description": "Qarsildoq baqlajonlar", "prep_time": "15 daqiqa", "image_url": "https://ibb.co/VZCZTrp", "composition": ["Баклажаны", "Соус"]},
            {"id": 50, "name": "Цезарь с курицей", "price": 45000, "description": "Sezar salati", "prep_time": "10 daqiqa", "image_url": "https://ibb.co/tP8T9WVg", "composition": ["Курица", "Салат", "Соус Цезарь"]},
            {"id": 51, "name": "Греческий салат", "price": 50000, "description": "Rukola bilan salat", "prep_time": "8 daqiqa", "image_url": "https://ibb.co/Nd38hmJQ", "composition": ["Овощи", "Сыр Фета", "Оливки"]},
            {"id": 52, "name": "Салат Руккола", "price": 40000, "description": "Rukola salati", "prep_time": "8 daqiqa", "image_url": "https://ibb.co/B5NY9D39", "composition": ["Руккола", "Помидоры", "Сыр"]},
            {"id": 53, "name": "Мужской Каприз", "price": 40000, "description": "Kapriz salati", "prep_time": "8 daqiqa", "image_url": "https://ibb.co/b5jt6yRR", "composition": ["Овощи", "Мясо", "Соус"]},
            {"id": 54, "name": "Чука Салат", "price": 35000, "description": "Fuka salati", "prep_time": "8 daqiqa", "image_url": "https://ibb.co/5xsnpW3c", "composition": ["Водоросли Чука", "Кунжут"]},
            {"id": 55, "name": "Тар-Тар", "price": 15000, "description": "Tar-Tar sousi bilan", "prep_time": "5 daqiqa", "image_url": "https://ibb.co/Q3dFbp3X", "composition": ["Соус Тар-Тар"]},
            {"id": 56, "name": "Куринние Рамэн", "price": 45000, "description": "Oddiy ramen", "prep_time": "18 daqiqa", "image_url": "https://ibb.co/5xYJbRfc", "composition": ["Лапша", "Бульон", "Овощи"]}
        ]
    },
    "pizza_burger": {
        "name": "🍕 ПИЦЦЕЙ С БУРГЕР",
        "emoji": "🍕",
        "products": [
            {"id": 57, "name": "Токио Микс 35см", "price": 90000, "description": "Tokio miks pizza 35sm", "prep_time": "25 daqiqa", "image_url": "https://ibb.co/zTJMDKQH", "composition": ["Пепперони", "Ветчина", "Грибы", "Оливки"]},
            {"id": 58, "name": "Кази 35см", "price": 90000, "description": "Bazi pizza 35sm", "prep_time": "25 daqiqa", "image_url": "https://ibb.co/HDC28VSN", "composition": ["Колбаски", "Овощи", "Сыр"]},
            {"id": 59, "name": "Микс 35см", "price": 85000, "description": "Aralash pizza 35sm", "prep_time": "22 daqiqa", "image_url": "https://ibb.co/QFZZTtp2", "composition": ["Ассорти мяса", "Овощи", "Сыр"]},
            {"id": 60, "name": "Пепперони 35см", "price": 80000, "description": "Pishloqli pizza 35sm", "prep_time": "20 daqiqa", "image_url": "https://ibb.co/TDh7Bz76", "composition": ["Пепперони", "Сыр"]},
            {"id": 61, "name": "Кузикорин 35см", "price": 80000, "description": "Kuzidirini pizza 35sm", "prep_time": "20 daqiqa", "image_url": "https://ibb.co/7th0vwxT", "composition": ["Курица", "Овощи", "Сыр"]},
            {"id": 62, "name": "Маргарита 35см", "price": 75000, "description": "Margarita pizza 35sm", "prep_time": "18 daqiqa", "image_url": "https://ibb.co/bMYmp7Kq", "composition": ["Помидоры", "Сыр", "Базилик"]},
            {"id": 63, "name": "Гамбургер", "price": 28000, "description": "Gamburger", "prep_time": "10 daqiqa", "image_url": "https://ibb.co/jksjJ4Jt", "composition": ["Говяжья котлета", "Овощи", "Соус"]},
            {"id": 64, "name": "Чизбургер", "price": 33000, "description": "Chizburger", "prep_time": "12 daqiqa", "image_url": "https://ibb.co/VWx6vgQK", "composition": ["Говяжья котлета", "Сыр", "Овощи"]},
            {"id": 65, "name": "Токио Бургер", "price": 37000, "description": "Tokio maxsus burger", "prep_time": "15 daqiqa", "image_url": "https://ibb.co/LhnynQdb", "composition": ["Говяжья котлета", "Сыр", "Овощи", "Специальный соус"]},
            {"id": 66, "name": "Куриные крылышки", "price": 35000, "description": "Qovurilgan tovuq qanotchalar", "prep_time": "15 daqiqa", "image_url": None, "composition": ["Куриные крылышки", "Соус"]},
            {"id": 67, "name": "Сырные шарики", "price": 22000, "description": "Pishloq shariklari", "prep_time": "8 daqiqa", "image_url": None, "composition": ["Сыр", "Панировка"]},
            {"id": 68, "name": "Картофель Фри", "price": 22000, "description": "Qovurilgan kartoshka", "prep_time": "7 daqiqa", "image_url": None, "composition": ["Картофель", "Соль"]},
            {"id": 69, "name": "Клаб Сендвич", "price": 35000, "description": "Klub sendvich", "prep_time": "10 daqiqa", "image_url": None, "composition": ["Курица", "Бекон", "Овощи", "Соус"]}
        ]
    },
    "napitki": {
        "name": "🥤 ИЧИМЛИКЛАР",
        "emoji": "🥤",
        "products": [
            {"id": 70, "name": "Мохито 1л", "price": 45000, "description": "Sovuq mojito", "prep_time": "3 daqiqa", "image_url": None, "composition": []},
            {"id": 71, "name": "Мохито 0.7л", "price": 25000, "description": "Sovuq mojito", "prep_time": "3 daqiqa", "image_url": None, "composition": []},
            {"id": 72, "name": "Мохито 0.5л", "price": 20000, "description": "Sovuq mojito", "prep_time": "3 daqiqa", "image_url": None, "composition": []},
            {"id": 73, "name": "Чай Чудо", "price": 35000, "description": "Maxsus choy", "prep_time": "2 daqiqa", "image_url": None, "composition": []},
            {"id": 74, "name": "Чай Токио", "price": 35000, "description": "Tokio maxsus choy", "prep_time": "2 daqiqa", "image_url": None, "composition": []},
            {"id": 75, "name": "Чай Фруктовый", "price": 35000, "description": "Mevali choy", "prep_time": "2 daqiqa", "image_url": None, "composition": []},
            {"id": 76, "name": "Чай Тархун", "price": 35000, "description": "Tarxun choyi", "prep_time": "2 daqiqa", "image_url": None, "composition": []},
            {"id": 77, "name": "Чай Багини", "price": 35000, "description": "Rayhon choyi", "prep_time": "2 daqiqa", "image_url": None, "composition": []},
            {"id": 78, "name": "Чай Каркаде", "price": 30000, "description": "Karkade choyi", "prep_time": "2 daqiqa", "image_url": None, "composition": []},
            {"id": 79, "name": "Чай Лимон", "price": 25000, "description": "Limonli choy", "prep_time": "2 daqiqa", "image_url": None, "composition": []},
            {"id": 80, "name": "Милкшейк Клубника", "price": 30000, "description": "Qulupnayli milkshake", "prep_time": "5 daqiqa", "image_url": None, "composition": []},
            {"id": 81, "name": "Милкшейк Сникерс", "price": 30000, "description": "Snickers milkshake", "prep_time": "5 daqiqa", "image_url": None, "composition": []},
            {"id": 82, "name": "Милкшейк Банан", "price": 30000, "description": "Bananli milkshake", "prep_time": "5 daqiqa", "image_url": None, "composition": []},
            {"id": 83, "name": "Милкшейк Орео", "price": 30000, "description": "Oreo milkshake", "prep_time": "5 daqiqa", "image_url": None, "composition": []},
            {"id": 84, "name": "Милкшейк Киви", "price": 30000, "description": "Kinder milkshake", "prep_time": "5 daqiqa", "image_url": None, "composition": []},
            {"id": 85, "name": "Кола 1л", "price": 14000, "description": "Gazlangan ichimlik 1L", "prep_time": "1 daqiqa", "image_url": None, "composition": []},
            {"id": 86, "name": "Фанта 1л", "price": 14000, "description": "Gazlangan ichimlik 1L", "prep_time": "1 daqiqa", "image_url": None, "composition": []},
            {"id": 87, "name": "Фюсти 1л", "price": 13000, "description": "Gazlangan ichimlik 1L", "prep_time": "1 daqiqa", "image_url": None, "composition": []},
            {"id": 88, "name": "Кола-Фанта Ж/Б", "price": 10000, "description": "Kola 0.5L", "prep_time": "1 daqiqa", "image_url": None, "composition": []},
            {"id": 89, "name": "Вода Без Газа", "price": 8000, "description": "Gazsiz suv", "prep_time": "1 daqiqa", "image_url": None, "composition": []},
            {"id": 90, "name": "Сок", "price": 19000, "description": "Tabiiy sok", "prep_time": "1 daqiqa", "image_url": None, "composition": []}
        ]
    }
}

# ==================== ASOSIY FUNKSIYALAR ====================

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

def language_selection(chat_id):
    """Tilni tanlash"""
    keyboard = {
        "keyboard": [
            ["🇺🇿 O'zbekcha", "🇷🇺 Русский"]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    
    text = """
🌍 <b>Выберите язык / Tilni tanlang</b>

Пожалуйста, выберите язык / Iltimos, tilni tanlang:
"""
    send_message(chat_id, text, keyboard)

def main_menu_with_language(chat_id):
    """Tilga qarab asosiy menyu"""
    lang = user_language.get(chat_id, "uz")
    
    if lang == "uz":
        if str(chat_id) == ADMIN_ID:
            keyboard = {
                "keyboard": [
                    ["🍽 Mazali Menyu", "🛒 Savat"],
                    ["📦 Mening buyurtmalarim", "ℹ️ Ma'lumotlar"],
                    ["✍️ Fikr qoldirish", "☎️ Bog'lanish"],
                    ["👑 Admin Panel"]
                ],
                "resize_keyboard": True
            }
        else:
            keyboard = {
                "keyboard": [
                    ["🍽 Mazali Menyu", "🛒 Savat"],
                    ["📦 Mening buyurtmalarim", "ℹ️ Ma'lumotlar"],
                    ["✍️ Fikr qoldirish", "☎️ Bog'lanish"]
                ],
                "resize_keyboard": True
            }
    else:
        if str(chat_id) == ADMIN_ID:
            keyboard = {
                "keyboard": [
                    ["🍽 Вкусное Меню", "🛒 Корзина"],
                    ["📦 Мои заказы", "ℹ️ Информация"],
                    ["✍️ Оставить отзыв", "☎️ Контакты"],
                    ["👑 Панель Администратора"]
                ],
                "resize_keyboard": True
            }
        else:
            keyboard = {
                "keyboard": [
                    ["🍽 Вкусное Меню", "🛒 Корзина"],
                    ["📦 Мои заказы", "ℹ️ Информация"],
                    ["✍️ Оставить отзыв", "☎️ Контакты"]
                ],
                "resize_keyboard": True
            }
    return keyboard

def send_welcome_message(chat_id):
    """Xush kelibsiz xabari"""
    lang = user_language.get(chat_id, "uz")
    
    if lang == "uz":
        text = """
👋 <b>Tokio sushi botiga xush kelibsiz!</b>

🍣 Sizni ko'rib turganimizdan xursandmiz! Boshlash uchun quyidagi menyudan birini tanlang:

🍽 <b>Menyu:</b> Bizning mazali va yangi taomlarimizga buyurtma bering.

✍️ <b>Fikr qoldirish:</b> Xizmatlarimiz haqida o'z fikringizni bildiring.

ℹ️ <b>Ma'lumotlar:</b> Bizning restoran haqida ko'proq bilib oling.

☎️ <b>Bog'lanish:</b> Savollaringiz bormi? Biz doimo aloqadamiz!

🌍 <b>Tilni o'zgartirish:</b> O'zingizga qulay tilni tanlang.
"""
    else:
        text = """
👋 <b>Добро пожаловать в бот Tokio sushi!</b>

🍣 Мы рады видеть вас! Выберите один из пунктов меню для начала:

🍽 <b>Меню:</b> Закажите наши вкусные и свежие блюда.

✍️ <b>Оставить отзыв:</b> Поделитесь своим мнением о наших услугах.

ℹ️ <b>Информация:</b> Узнайте больше о нашем ресторане.

☎️ <b>Контакты:</b> Есть вопросы? Мы всегда на связи!

🌍 <b>Сменить язык:</b> Выберите удобный для вас язык.
"""
    
    send_message(chat_id, text, main_menu_with_language(chat_id))

def show_full_menu(chat_id):
    """To'liq menyuni ko'rsatish"""
    lang = user_language.get(chat_id, "uz")
    
    if lang == "uz":
        text = """
🍽 <b>Mazali Menyu</b>

Assalomu alaykum! Menyuga xush kelibsiz.

Nimadan boshlaymiz?

Ovqatga buyurtma berish uchun biror kategoriya tanlang:
"""
    else:
        text = """
🍽 <b>Вкусное Меню</b>

Ассалому алайкум! Добро пожаловать в меню.

С чего начнем?

Выберите категорию для заказа еды:
"""
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "🍣 ХОЛОДНЫЕ РОЛЛЫ", "callback_data": "category_holodnye_rolly"}],
            [{"text": "🔥 ЗАПЕЧЕННЫЕ ФИРМЕННЫЕ РОЛЛЫ ОТ:", "callback_data": "category_zapechennye"}],
            [{"text": "⚡ ЖАРЕНЫЕ РОЛЛЫ", "callback_data": "category_jarennye_rolly"}],
            [{"text": "🎎 СЕТЛАР", "callback_data": "category_sety"}],
            [{"text": "🍱 СУШИ ВА ГУНКАН", "callback_data": "category_sushi_gunkan"}],
            [{"text": "🍜 ГОРЯЧАЯ ЕДА", "callback_data": "category_goryachaya_eda"}],
            [{"text": "🍕 ПИЦЦЕЙ С БУРГЕР", "callback_data": "category_pizza_burger"}],
            [{"text": "🥤 ИЧИМЛИКЛАР", "callback_data": "category_napitki"}],
            [{"text": "🛒 Savatni ko'rish", "callback_data": "view_cart"}],
            [{"text": "🏠 Asosiy menyu", "callback_data": "main_menu"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def show_category(chat_id, category_key):
    """Kategoriyani ko'rsatish"""
    category = menu_data[category_key]
    lang = user_language.get(chat_id, "uz")
    
    if lang == "uz":
        text = f"""
🍽 <b>Mazali Menyu</b>

Assalomu alaykum! Menyuga xush kelibsiz.

Nimadan boshlaymiz?

<b>{category['name']}</b>

Ovqatga buyurtma berish uchun biror mahsulot tanlang:
"""
    else:
        text = f"""
🍽 <b>Вкусное Меню</b>

Ассалому алайкум! Добро пожаловать в меню.

С чего начнем?

<b>{category['name']}</b>

Выберите любой продукт для заказа еды:
"""
    
    keyboard = {"inline_keyboard": []}
    
    # Mahsulotlar - faqat nomlari
    for product in category["products"]:
        keyboard["inline_keyboard"].append([
            {"text": product['name'], "callback_data": f"view_{product['id']}"}
        ])
    
    # Navigatsiya tugmalari
    if lang == "uz":
        keyboard["inline_keyboard"].extend([
            [{"text": "🛒 Savatni ko'rish", "callback_data": "view_cart"}],
            [{"text": "📋 Bosh menyu", "callback_data": "show_menu"}],
            [{"text": "🏠 Asosiy menyu", "callback_data": "main_menu"}]
        ])
    else:
        keyboard["inline_keyboard"].extend([
            [{"text": "🛒 Корзина", "callback_data": "view_cart"}],
            [{"text": "📋 Главное меню", "callback_data": "show_menu"}],
            [{"text": "🏠 Главное меню", "callback_data": "main_menu"}]
        ])
    
    send_message(chat_id, text, keyboard)

def view_product(chat_id, product_id):
    """Mahsulotni ko'rsatish"""
    # Mahsulotni topish
    product = None
    category_key = None
    for cat_key, category in menu_data.items():
        for p in category["products"]:
            if p["id"] == product_id:
                product = p
                category_key = cat_key
                break
        if product:
            break
    
    if not product:
        send_message(chat_id, "❌ Mahsulot topilmadi")
        return
    
    lang = user_language.get(chat_id, "uz")
    
    # Tarkibni formatlash
    composition_text = ""
    if "composition" in product and product["composition"]:
        for item in product["composition"]:
            composition_text += f"• {item}\n"
    
    if lang == "uz":
        caption = f"""
🍣 <b>{product['name']}</b>

{composition_text}
💰 <b>Narxi:</b> {product['price']:,} so'm
⏱️ <b>Tayyorlanish vaqti:</b> {product['prep_time']}
📝 <b>Tavsif:</b> {product['description']}
"""
    else:
        caption = f"""
🍣 <b>{product['name']}</b>

{composition_text}
💰 <b>Цена:</b> {product['price']:,} сум
⏱️ <b>Время приготовления:</b> {product['prep_time']}
📝 <b>Описание:</b> {product['description']}
"""
    
    # Miqdor tanlash keyboard
    if lang == "uz":
        keyboard = {
            "inline_keyboard": [
                [{"text": "1", "callback_data": f"add_qty_{product_id}_1"}, 
                 {"text": "2", "callback_data": f"add_qty_{product_id}_2"},
                 {"text": "3", "callback_data": f"add_qty_{product_id}_3"}],
                [{"text": "4", "callback_data": f"add_qty_{product_id}_4"},
                 {"text": "5", "callback_data": f"add_qty_{product_id}_5"},
                 {"text": "6", "callback_data": f"add_qty_{product_id}_6"}],
                [{"text": "➕ Savatga qo'shish", "callback_data": f"add_{product_id}"}],
                [{"text": "⬅️ Ortga", "callback_data": f"category_{category_key}"}]
            ]
        }
    else:
        keyboard = {
            "inline_keyboard": [
                [{"text": "1", "callback_data": f"add_qty_{product_id}_1"}, 
                 {"text": "2", "callback_data": f"add_qty_{product_id}_2"},
                 {"text": "3", "callback_data": f"add_qty_{product_id}_3"}],
                [{"text": "4", "callback_data": f"add_qty_{product_id}_4"},
                 {"text": "5", "callback_data": f"add_qty_{product_id}_5"},
                 {"text": "6", "callback_data": f"add_qty_{product_id}_6"}],
                [{"text": "➕ В корзину", "callback_data": f"add_{product_id}"}],
                [{"text": "⬅️ Назад", "callback_data": f"category_{category_key}"}]
            ]
        }
    
    # Rasm mavjud bo'lsa, rasm yuboramiz
    if product.get("image_url"):
        send_photo(chat_id, product["image_url"], caption, keyboard)
    else:
        # Ichimliklar uchun oddiy matn
        send_message(chat_id, caption, keyboard)

def add_to_cart(chat_id, product_id, quantity=1):
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
    
    # Savatga berilgan miqdorda qo'shish
    for _ in range(quantity):
        user_data[chat_id]["cart"].append(product)
    
    lang = user_language.get(chat_id, "uz")
    
    if lang == "uz":
        text = f"""
✅ <b>SAVATGA QO'SHILDI</b>

🍣 {product['name']}
💰 Narxi: {product['price']:,} so'm
📦 Miqdor: {quantity} ta
⏱️ Tayyorlanish: {product['prep_time']}

🛒 Savatdagi mahsulotlar: {len(user_data[chat_id]['cart'])} ta
"""
    else:
        text = f"""
✅ <b>ДОБАВЛЕНО В КОРЗИНУ</b>

🍣 {product['name']}
💰 Цена: {product['price']:,} сум
📦 Количество: {quantity} шт
⏱️ Приготовление: {product['prep_time']}

🛒 Товаров в корзине: {len(user_data[chat_id]['cart'])} шт
"""
    
    if lang == "uz":
        keyboard = {
            "inline_keyboard": [
                [{"text": "🛒 Savatni ko'rish", "callback_data": "view_cart"}],
                [{"text": "📋 Menyu", "callback_data": "show_menu"}],
                [{"text": "✅ Buyurtma berish", "callback_data": "place_order"}]
            ]
        }
    else:
        keyboard = {
            "inline_keyboard": [
                [{"text": "🛒 Корзина", "callback_data": "view_cart"}],
                [{"text": "📋 Меню", "callback_data": "show_menu"}],
                [{"text": "✅ Оформить заказ", "callback_data": "place_order"}]
            ]
        }
    
    send_message(chat_id, text, keyboard)

def show_cart(chat_id):
    """Savatni ko'rsatish"""
    if chat_id not in user_data or "cart" not in user_data[chat_id] or not user_data[chat_id]["cart"]:
        lang = user_language.get(chat_id, "uz")
        if lang == "uz":
            send_message(chat_id, "🛒 <b>Sizning savatingiz bo'sh</b>\n\nIltimos, menyudan mahsulot tanlang!")
        else:
            send_message(chat_id, "🛒 <b>Ваша корзина пуста</b>\n\nПожалуйста, выберите продукты из меню!")
        return
    
    cart = user_data[chat_id]["cart"]
    total = sum(item['price'] for item in cart)
    
    # 20% chegirma hisoblash
    discount_amount = total * DISCOUNT_PERCENT // 100
    total_with_discount = total - discount_amount
    total_with_delivery = total_with_discount + DELIVERY_PRICE
    
    lang = user_language.get(chat_id, "uz")
    
    if lang == "uz":
        text = "🛒 <b>SAVATINGIZ</b>\n\n"
        for i, item in enumerate(cart, 1):
            text += f"{i}. {item['name']} - {item['price']:,} so'm\n"
        
        text += f"\n💵 Mahsulotlar: {total:,} so'm"
        text += f"\n🎁 Chegirma ({DISCOUNT_PERCENT}%): -{discount_amount:,} so'm"
        text += f"\n💳 Chegirma bilan: {total_with_discount:,} so'm"
        text += f"\n🚚 Yetkazib berish: {DELIVERY_PRICE:,} so'm"
        text += f"\n💰 <b>JAMI: {total_with_delivery:,} so'm</b>"
        text += f"\n⏰ Tayyorlanish vaqti: {PREPARATION_TIME}"
    else:
        text = "🛒 <b>ВАША КОРЗИНА</b>\n\n"
        for i, item in enumerate(cart, 1):
            text += f"{i}. {item['name']} - {item['price']:,} сум\n"
        
        text += f"\n💵 Товары: {total:,} сум"
        text += f"\n🎁 Скидка ({DISCOUNT_PERCENT}%): -{discount_amount:,} сум"
        text += f"\n💳 Со скидкой: {total_with_discount:,} сум"
        text += f"\n🚚 Доставка: {DELIVERY_PRICE:,} сум"
        text += f"\n💰 <b>ИТОГО: {total_with_delivery:,} сум</b>"
        text += f"\n⏰ Время приготовления: {PREPARATION_TIME}"
    
    if lang == "uz":
        keyboard = {
            "inline_keyboard": [
                [{"text": "✅ BUYURTMA BERISH", "callback_data": "place_order"}],
                [{"text": "🗑 Savatni tozalash", "callback_data": "clear_cart"}],
                [{"text": "📋 Menyuni ko'rish", "callback_data": "show_menu"}],
                [{"text": "🏠 Asosiy menyu", "callback_data": "main_menu"}]
            ]
        }
    else:
        keyboard = {
            "inline_keyboard": [
                [{"text": "✅ ОФОРМИТЬ ЗАКАЗ", "callback_data": "place_order"}],
                [{"text": "🗑 Очистить корзину", "callback_data": "clear_cart"}],
                [{"text": "📋 Посмотреть меню", "callback_data": "show_menu"}],
                [{"text": "🏠 Главное меню", "callback_data": "main_menu"}]
            ]
        }
    
    send_message(chat_id, text, keyboard)

def request_contact_and_location(chat_id):
    """Telefon raqam va lokatsiya so'rash"""
    request_contact(chat_id)

def request_contact(chat_id):
    """Telefon raqam so'rash"""
    # Oldingi ma'lumotlarni tozalash
    if chat_id in user_data:
        user_data[chat_id].pop("phone", None)
        user_data[chat_id].pop("location", None)
        user_data[chat_id].pop("location_type", None)
    
    lang = user_language.get(chat_id, "uz")
    
    if lang == "uz":
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
"Iltimos, \"📞 Telefon raqamni yuborish\" tugmasini bosing.
"""
    else:
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
    """Lokatsiya so'rash"""
    lang = user_language.get(chat_id, "uz")
    
    if lang == "uz":
        keyboard = {
            "keyboard": [
                [{
                    "text": "📍 Google Maps orqali",
                    "request_location": True
                }],
                [{
                    "text": "🌐 Yandex Maps havolasini yuborish"
                }],
                ["🏠 Asosiy menyu"]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": True
        }
        
        text = """
📍 <b>MANZILINGIZNI YUBORING</b>

Yetkazib berish uchun manzilingizni yuboring.

<b>Variantlar:</b>
• "📍 Google Maps orqali" - joylashuvingizni yuboring
• "🌐 Yandex Maps havolasini yuborish" - Yandex Maps havolasini yuboring
• Yoki aniq manzilni matn shaklida yozing

📝 <i>Masalan: Karshi shahar, Amir Temur ko'chasi, 45-uy</i>
"""
    else:
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
    lang = user_language.get(chat_id, "uz")
    
    if lang == "uz":
        keyboard = {
            "keyboard": [
                ["💳 Karta orqali to'lash", "💵 Naqd pul"],
                ["🏠 Asosiy menyu"]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": True
        }
        
        text = """
💳 <b>TO'LOV USULINI TANLANG</b>

Iltimos, qulay to'lov usulini tanlang:

• <b>💳 Karta orqali to'lash</b> - kartaga o'tkazma
• <b>💵 Naqd pul</b> - yetkazib berish vaqtida naqd pul
"""
    else:
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
    lang = user_language.get(chat_id, "uz")
    
    if lang == "uz":
        text = f"""
💳 <b>KARTA ORQALI TO'LOV</b>

📦 Buyurtma raqami: #{order_id}
💰 To'lov summasi: {order['total_with_delivery']:,} so'm

<b>Karta ma'lumotlari:</b>
💳 Karta raqami: <code>{CARD_NUMBER}</code>
👤 Karta egasi: {CARD_HOLDER}

💡 <b>To'lovni amalga oshirgach, chek skrinshotini yuboring</b>

✅ To'lov tasdiqlangach, buyurtmangiz tayyorlanadi.
"""
    else:
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
    
    if lang == "uz":
        keyboard = {
            "inline_keyboard": [
                [{"text": "✅ To'lov qildim", "callback_data": f"payment_done_{order_id}"}],
                [{"text": "🏠 Asosiy menyu", "callback_data": "main_menu"}]
            ]
        }
    else:
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
    lang = user_language.get(chat_id, "uz")
    
    if lang == "uz":
        text = f"""
💵 <b>NAQD TO'LOV TASDIQLANDI</b>

📦 Buyurtma raqami: #{order_id}
💰 To'lov summasi: {order['total_with_delivery']:,} so'm
✅ To'lov usuli: Naqd pul

🎉 Buyurtmangiz qabul qilindi va tayyorlanmoqda!
⏰ Tayyorlanish vaqti: {PREPARATION_TIME}

📞 Aloqa: +998 91 211 12 15
"""
    else:
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
    orders_data[order_id]["status"] = "qabul qilindi"
    orders_data[order_id]["payment_method"] = "naqd pul"
    orders_data[order_id]["payment_status"] = "kutilmoqda"
    
    send_message(chat_id, text, main_menu_with_language(chat_id))
    
    # Adminga naqd to'lov haqida xabar
    admin_text = f"""
💵 <b>NAQD TO'LOV - BUYURTMA #{order_id}</b>

👤 Mijoz ID: {order['user_id']}
📞 Telefon: {order['user_phone']}
💰 Summa: {order['total_with_delivery']:,} so'm
📍 Manzil: {order['user_location']}
🗺️ Xarita turi: {order['location_type']}

✅ To'lov usuli: Naqd pul
🔄 Holat: To'lov kutilmoqda
"""
    
    admin_keyboard = {
        "inline_keyboard": [
            [{"text": "✅ To'lov qilindi", "callback_data": f"cash_paid_{order_id}"}],
            [{"text": "❌ Bekor qilish", "callback_data": f"cancel_{order_id}"}]
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
    """Buyurtmani adminga yuborish"""
    order = orders_data[order_id]
    
    # Xarita linklarini yaratish
    google_link, yandex_link = create_maps_links(
        order["user_location"], 
        order["location_type"]
    )
    
    payment_method = order.get("payment_method", "Tanlanmagan")
    payment_status = order.get("payment_status", "kutilmoqda")
    
    admin_text = f"""
🆕 <b>YANGI BUYURTMA</b> #{order_id}

👤 Mijoz ID: {order['user_id']}
📞 Telefon: {order['user_phone']}
📍 Manzil: {order['user_location']}
🗺️ Xarita turi: {order['location_type']}

🗺️ <b>XARITA HAVOLALARI:</b>
📍 Google Maps: {google_link}
🌐 Yandex Maps: {yandex_link}

💵 Mahsulotlar: {order['total']:,} so'm
🎁 Chegirma ({DISCOUNT_PERCENT}%): -{order['discount_amount']:,} so'm
💳 Chegirma bilan: {order['total_with_discount']:,} so'm
🚚 Yetkazib berish: {DELIVERY_PRICE:,} so'm
💰 <b>JAMI: {order['total_with_delivery']:,} so'm</b>

💳 To'lov usuli: {payment_method}
🔄 To'lov holati: {payment_status}
⏰ Vaqt: {get_uzbekistan_time().strftime('%H:%M')}

📦 <b>Buyurtma tarkibi:</b>
"""
    for i, item in enumerate(order["items"], 1):
        admin_text += f"{i}. {item['name']} - {item['price']:,} so'm\n"
    
    admin_keyboard = {
        "inline_keyboard": [
            [{"text": "✅ Qabul qilish", "callback_data": f"accept_{order_id}"}],
            [{"text": "❌ Bekor qilish", "callback_data": f"cancel_{order_id}"}],
            [{"text": "✅ Buyurtma tayyor", "callback_data": f"ready_{order_id}"}],
            [{"text": "📞 Mijoz bilan bog'lanish", "callback_data": f"contact_{order_id}"}],
            [{"text": "🗺️ Xarita havolalari", "callback_data": f"maps_{order_id}"}]
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
🗺️ <b>XARITA HAVOLALARI - BUYURTMA #{order_id}</b>

📍 <b>Google Maps:</b>
{google_link}

🌐 <b>Yandex Maps:</b>
{yandex_link}

👤 Mijoz: {order['user_phone']}
📍 Manzil: {order['user_location']}
"""
    
    send_message(ADMIN_ID, maps_text)

def process_order(chat_id):
    """Buyurtmani qayta ishlash"""
    if chat_id not in user_data or "cart" not in user_data[chat_id] or not user_data[chat_id]["cart"]:
        lang = user_language.get(chat_id, "uz")
        if lang == "uz":
            send_message(chat_id, "❌ Sizning savatingiz bo'sh")
        else:
            send_message(chat_id, "❌ Ваша корзина пуста")
        return
    
    # Har safar telefon va lokatsiya so'rash
    request_contact_and_location(chat_id)

def create_order_from_cart(chat_id):
    """Savatdagi mahsulotlardan buyurtma yaratish"""
    if chat_id not in user_data or "cart" not in user_data[chat_id] or not user_data[chat_id]["cart"]:
        lang = user_language.get(chat_id, "uz")
        if lang == "uz":
            send_message(chat_id, "❌ Sizning savatingiz bo'sh")
        else:
            send_message(chat_id, "❌ Ваша корзина пуста")
        return
    
    if "phone" not in user_data[chat_id] or "location" not in user_data[chat_id]:
        lang = user_language.get(chat_id, "uz")
        if lang == "uz":
            send_message(chat_id, "❌ Telefon raqami yoki manzil ma'lumotlari yetarli emas")
        else:
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
        "status": "yangi",
        "payment_method": None,
        "payment_status": "kutilmoqda",
        "timestamp": get_uzbekistan_time().isoformat()
    }
    
    # Savatni tozalash
    user_data[chat_id]["cart"] = []
    
    # To'lov usulini so'rash
    request_payment_method(chat_id)

# ==================== FIKR-MULOHAZA TIZIMI ====================

def start_feedback(chat_id):
    """Fikr-mulohaza qoldirishni boshlash"""
    lang = user_language.get(chat_id, "uz")
    
    if lang == "uz":
        text = """
Sushi Yummyni tanlaganingiz uchun rahmat!

Agar xizmatlarimizni baholab, bizga yordam bersangiz, sizga minnatdor bo'lamiz!

5 ballik tizimda baholang.
"""
    else:
        text = """
Спасибо, что выбрали Sushi Yummy!

Если вы оцените наши услуги и поможете нам, мы будем благодарны вам!

Оцените по 5-балльной системе.
"""
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "⭐️⭐️⭐️⭐️⭐️ajoyib", "callback_data": "rate_5"}],
            [{"text": "⭐️⭐️⭐️⭐️yaxshi", "callback_data": "rate_4"}],
            [{"text": "⭐️⭐️⭐️qoniqarli", "callback_data": "rate_3"}],
            [{"text": "⭐️⭐️unchamas", "callback_data": "rate_2"}],
            [{"text": "⭐️juda yomon", "callback_data": "rate_1"}],
            [{"text": "🏠 Menu", "callback_data": "main_menu"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def ask_service_issue(chat_id, rating):
    """Qaysi xizmat yoqmaganini so'rash"""
    lang = user_language.get(chat_id, "uz")
    
    if lang == "uz":
        text = f"""
Qaysi xizmat turi sizga yoqmadi?
"""
    else:
        text = f"""
Какой тип услуги вам не понравился?
"""
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "Yetkazib berish", "callback_data": f"issue_delivery_{rating}"}],
            [{"text": "Mahsulot sifati", "callback_data": f"issue_quality_{rating}"}],
            [{"text": "Xodimlar xizmati", "callback_data": f"issue_service_{rating}"}],
            [{"text": "Narxlar", "callback_data": f"issue_prices_{rating}"}],
            [{"text": "Boshqa", "callback_data": f"issue_other_{rating}"}],
            [{"text": "⬅️ Ortga", "callback_data": "feedback_back"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def thank_for_feedback(chat_id, rating, issue=None):
    """Fikr uchun rahmat"""
    lang = user_language.get(chat_id, "uz")
    
    if lang == "uz":
        text = f"""
Rahmat! Sizning bahoingiz: {rating}/5
"""
        if issue:
            text += f"\nMuammo: {issue}"
        
        text += "\nFikringiz uchun rahmat!"
    else:
        text = f"""
Спасибо! Ваша оценка: {rating}/5
"""
        if issue:
            text += f"\nПроблема: {issue}"
        
        text += "\nСпасибо за ваш отзыв!"
    
    # Fikrni ma'lumotlar bazasiga saqlash
    if chat_id not in user_feedback:
        user_feedback[chat_id] = []
    
    user_feedback[chat_id].append({
        "rating": rating,
        "issue": issue,
        "timestamp": get_uzbekistan_time().isoformat()
    })
    
    send_message(chat_id, text, main_menu_with_language(chat_id))

# ==================== MA'LUMOTLAR VA BOG'LANISH ====================

def show_info(chat_id):
    """Ma'lumotlar bo'limi"""
    lang = user_language.get(chat_id, "uz")
    
    if lang == "uz":
        text = """
🏮 <b>TOKIO SUSHI HAQIDA MA'LUMOT</b>

📍 <b>Manzil:</b> 
g. Karshi, Amir Temur ko'chasi, 45
(Asosiy bozor yonida)

🕒 <b>Ish vaqti:</b>
Dushanba-Yakshanba: 11:00 - 02:00

🚚 <b>Yetkazib berish:</b>
• Yetkazib berish narxi: 10,000 so'm
• Tayyorlanish vaqti: 30-45 daqiqa
• Yetkazib berish muddati: 45-60 daqiqa

🍣 <b>Biz haqimizda:</b>
Tokio Sushi - bu an'anaviy yapon oshxonasining eng yaxshi an'analarini zamonaviy uslubda taqdim etadigan premium restoran. Biz eng yangi va sifatli mahsulotlardan foydalanamiz.

⭐ <b>Afzalliklarimiz:</b>
• 98 xil premium mahsulot
• Har bir buyurtmaga 20% chegirma
• Tez va sifatli xizmat
• Bepul maslahat

📞 <b>Aloqa:</b>
+998 91 211 12 15

📍 <b>Lokatsiya:</b>
https://maps.app.goo.gl/KmfJA59T36FgRzWZ6
"""
    else:
        text = """
🏮 <b>ИНФОРМАЦИЯ О TOKIO SUSHI</b>

📍 <b>Адрес:</b>
г. Карши, ул. ул.Узбекитан 45
(Рядом с урин бобо чайхана)

🕒 <b>Время работы:</b>
Понедельник-Воскресенье: 11:00 - 02:00

🚚 <b>Доставка:</b>
• Стоимость доставки: 10,000 сум
• Время приготовления: 30-45 минут
• Время доставки: 45-60 минут

🍣 <b>О нас:</b>
Tokio Sushi - это премиальный ресторан, который представляет лучшие традиции японской кухни в современном стиле. Мы используем самые свежие и качественные продукты.

⭐ <b>Наши преимущества:</b>
• 98 премиум продуктов
• Скидка 20% на каждый заказ
• Быстрое и качественное обслуживание
• Бесплатная консультация

📞 <b>Контакты:</b>
+998 91 211 12 15


📍 <b>Локация:</b>
https://maps.app.goo.gl/KmfJA59T36FgRzWZ6
"""
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "📍 Lokatsiya", "url": "https://maps.google.com/?q=Karshi+Amir+Temur+45"}],
            [{"text": "📞 Qo'ng'iroq qilish", "callback_data": "call_restaurant"}],
            [{"text": "🏠 Asosiy menyu", "callback_data": "main_menu"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def show_contacts(chat_id):
    """Bog'lanish bo'limi"""
    lang = user_language.get(chat_id, "uz")
    
    if lang == "uz":
        text = "❓ Savollaringiz bormi? Biz bilan bog'laning: +998 91 211 12 15"
    else:
        text = "❓ Есть вопросы? Свяжитесь с нами: +998 91 211 12 15"
    
    keyboard = {
        "inline_keyboard": [
            [{"text": "📞 Qo'ng'iroq qilish", "callback_data": "call_restaurant"}],
            [{"text": "📍 Lokatsiya", "url": "https://maps.google.com/?q=Karshi+Amir+Temur+45"}],
            [{"text": "🏠 Asosiy menyu", "callback_data": "main_menu"}]
        ]
    }
    
    send_message(chat_id, text, keyboard)

def change_language(chat_id):
    """Tilni o'zgartirish"""
    keyboard = {
        "keyboard": [
            ["🇺🇿 O'zbekcha", "🇷🇺 Русский"],
            ["🏠 Asosiy menyu"]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    
    lang = user_language.get(chat_id, "uz")
    
    if lang == "uz":
        text = "🌍 <b>Tilni o'zgartirish</b>\n\nIltimos, yangi tilni tanlang:"
    else:
        text = "🌍 <b>Сменить язык</b>\n\nПожалуйста, выберите новый язык:"
    
    send_message(chat_id, text, keyboard)

# ==================== CALLBACK QAYTA ISHLASH ====================

def handle_callback(chat_id, callback_data):
    """Callbacklarni qayta ishlash"""
    try:
        if callback_data.startswith("add_"):
            product_id = int(callback_data.split("_")[1])
            add_to_cart(chat_id, product_id)
            
        elif callback_data.startswith("add_qty_"):
            parts = callback_data.split("_")
            product_id = int(parts[2])
            quantity = int(parts[3])
            add_to_cart(chat_id, product_id, quantity)
            
        elif callback_data == "view_cart":
            show_cart(chat_id)
            
        elif callback_data == "place_order":
            process_order(chat_id)
            
        elif callback_data == "clear_cart":
            if chat_id in user_data:
                user_data[chat_id]["cart"] = []
            lang = user_language.get(chat_id, "uz")
            if lang == "uz":
                send_message(chat_id, "🗑 Savat tozalandi", main_menu_with_language(chat_id))
            else:
                send_message(chat_id, "🗑 Корзина очищена", main_menu_with_language(chat_id))
            
        elif callback_data == "show_menu":
            show_full_menu(chat_id)
            
        elif callback_data.startswith("category_"):
            category_key = callback_data.split("_", 1)[1]
            show_category(chat_id, category_key)
            
        elif callback_data.startswith("view_"):
            product_id = int(callback_data.split("_")[1])
            view_product(chat_id, product_id)
            
        elif callback_data == "main_menu":
            send_message(chat_id, "🏠 Asosiy menyu", main_menu_with_language(chat_id))
            
        elif callback_data.startswith("payment_done_"):
            order_id = int(callback_data.split("_")[2])
            lang = user_language.get(chat_id, "uz")
            if lang == "uz":
                text = f"""
✅ <b>TO'LOV MA'LUMOTLARI QABUL QILINDI</b>

📦 Buyurtma raqami: #{order_id}
💳 Iltimos, chek skrinshotini yuboring.

⏳ To'lov tasdiqlangach, buyurtmangiz tayyorlanadi.
📞 Aloqa: +998 91 211 12 15
"""
            else:
                text = f"""
✅ <b>ИНФОРМАЦИЯ ОБ ОПЛАТЕ ПРИНЯТА</b>

📦 Номер заказа: #{order_id}
💳 Пожалуйста, отправьте скриншот чека.

⏳ После подтверждения оплаты ваш заказ будет приготовлен.
📞 Связь: +998 91 211 12 15
"""
            send_message(chat_id, text, main_menu_with_language(chat_id))
            
        elif callback_data.startswith("accept_"):
            if str(chat_id) == ADMIN_ID:
                order_id = int(callback_data.split("_")[1])
                if order_id in orders_data:
                    orders_data[order_id]["status"] = "qabul qilindi"
                    user_id = orders_data[order_id]["user_id"]
                    lang = user_language.get(user_id, "uz")
                    if lang == "uz":
                        send_message(user_id, f"✅ #{order_id} raqamli buyurtma qabul qilindi va tayyorlanmoqda!")
                    else:
                        send_message(user_id, f"✅ Заказ #{order_id} принят и готовится!")
                    send_message(chat_id, f"✅ #{order_id} raqamli buyurtma qabul qilindi")
            
        elif callback_data.startswith("ready_"):
            if str(chat_id) == ADMIN_ID:
                order_id = int(callback_data.split("_")[1])
                if order_id in orders_data:
                    orders_data[order_id]["status"] = "tayyor"
                    user_id = orders_data[order_id]["user_id"]
                    lang = user_language.get(user_id, "uz")
                    if lang == "uz":
                        send_message(user_id, f"🎉 #{order_id} raqamli buyurtma tayyor! Yetkazib berilmoqda...")
                    else:
                        send_message(user_id, f"🎉 Заказ #{order_id} готов! Доставляется...")
                    send_message(chat_id, f"✅ #{order_id} raqamli buyurtma tayyor deb belgilandi")
            
        elif callback_data.startswith("cancel_"):
            if str(chat_id) == ADMIN_ID:
                order_id = int(callback_data.split("_")[1])
                if order_id in orders_data:
                    orders_data[order_id]["status"] = "bekor qilindi"
                    user_id = orders_data[order_id]["user_id"]
                    lang = user_language.get(user_id, "uz")
                    if lang == "uz":
                        send_message(user_id, f"❌ #{order_id} raqamli buyurtma bekor qilindi. Iltimos, qayta urinib ko'ring.")
                    else:
                        send_message(user_id, f"❌ Заказ #{order_id} отменен. Пожалуйста, попробуйте снова.")
                    send_message(chat_id, f"❌ #{order_id} raqamli buyurtma bekor qilindi")
            
        elif callback_data.startswith("contact_"):
            if str(chat_id) == ADMIN_ID:
                order_id = int(callback_data.split("_")[1])
                if order_id in orders_data:
                    user_id = orders_data[order_id]["user_id"]
                    user_phone = orders_data[order_id]["user_phone"]
                    send_message(chat_id, f"📞 #{order_id} raqamli buyurtma uchun mijoz telefon raqami: {user_phone}")
            
        elif callback_data.startswith("maps_"):
            if str(chat_id) == ADMIN_ID:
                order_id = int(callback_data.split("_")[1])
                if order_id in orders_data:
                    send_maps_links_to_admin(order_id)
            
        elif callback_data.startswith("cash_paid_"):
            if str(chat_id) == ADMIN_ID:
                order_id = int(callback_data.split("_")[2])
                if order_id in orders_data:
                    orders_data[order_id]["payment_status"] = "to'landi"
                    orders_data[order_id]["status"] = "qabul qilindi"
                    user_id = orders_data[order_id]["user_id"]
                    lang = user_language.get(user_id, "uz")
                    if lang == "uz":
                        send_message(user_id, f"✅ #{order_id} raqamli buyurtma uchun to'lov qabul qilindi va buyurtma tayyorlanmoqda!")
                    else:
                        send_message(user_id, f"✅ Оплата для заказа #{order_id} получена и заказ готовится!")
                    send_message(chat_id, f"✅ #{order_id} raqamli buyurtma uchun to'lov tasdiqlandi")
                    
        # Fikr-mulohaza callbacklari
        elif callback_data.startswith("rate_"):
            rating = int(callback_data.split("_")[1])
            
            if rating <= 3:
                ask_service_issue(chat_id, rating)
            else:
                thank_for_feedback(chat_id, rating)

        elif callback_data.startswith("issue_"):
            parts = callback_data.split("_")
            issue_type = parts[1]
            rating = int(parts[2])
            
            issue_map = {
                "delivery": "Yetkazib berish",
                "quality": "Mahsulot sifati", 
                "service": "Xodimlar xizmati",
                "prices": "Narxlar",
                "other": "Boshqa"
            }
            
            issue = issue_map.get(issue_type, "Boshqa")
            thank_for_feedback(chat_id, rating, issue)

        elif callback_data == "feedback_back":
            start_feedback(chat_id)
            
        elif callback_data == "call_restaurant":
            lang = user_language.get(chat_id, "uz")
            if lang == "uz":
                send_message(chat_id, "📞 Qo'ng'iroq qilish uchun: +998 91 211 12 15")
            else:
                send_message(chat_id, "📞 Для звонка: +998 91 211 12 15")
                    
    except Exception as e:
        print(f"Ошибка callback: {e}")
        lang = user_language.get(chat_id, "uz")
        if lang == "uz":
            send_message(chat_id, "❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        else:
            send_message(chat_id, "❌ Произошла ошибка. Пожалуйста, попробуйте снова.")

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
                                # Foydalanuvchi tilini sozlash
                                if chat_id not in user_language:
                                    user_language[chat_id] = "uz"
                                language_selection(chat_id)
                            
                            elif text == "🇺🇿 O'zbekcha":
                                user_language[chat_id] = "uz"
                                send_message(chat_id, "✅ Til o'zbekchaga o'zgartirildi", main_menu_with_language(chat_id))
                                
                            elif text == "🇷🇺 Русский":
                                user_language[chat_id] = "ru"
                                send_message(chat_id, "✅ Язык изменен на русский", main_menu_with_language(chat_id))
                            
                            elif text == "🍽 Mazali Menyu" or text == "🍽 Вкусное Меню":
                                show_full_menu(chat_id)
                            
                            elif text == "🛒 Savat" or text == "🛒 Корзина":
                                show_cart(chat_id)
                                
                            elif text == "📦 Mening buyurtmalarim" or text == "📦 Мои заказы":
                                user_orders = [order for order in orders_data.values() if order["user_id"] == chat_id]
                                lang = user_language.get(chat_id, "uz")
                                if user_orders:
                                    if lang == "uz":
                                        text = "📦 <b>BUYURTMALARINGIZ</b>\n\n"
                                    else:
                                        text = "📦 <b>ВАШИ ЗАКАЗЫ</b>\n\n"
                                    for order in user_orders[-5:]:
                                        status_emoji = "✅" if order["status"] == "tayyor" else "⏳" if order["status"] == "qabul qilindi" else "❌"
                                        order_id = list(orders_data.keys())[list(orders_data.values()).index(order)]
                                        if lang == "uz":
                                            text += f"{status_emoji} #{order_id} - {order['total_with_delivery']:,} so'm - {order['status']}\n"
                                        else:
                                            text += f"{status_emoji} #{order_id} - {order['total_with_delivery']:,} сум - {order['status']}\n"
                                    send_message(chat_id, text)
                                else:
                                    if lang == "uz":
                                        send_message(chat_id, "📦 Hali buyurtmalaringiz yo'q")
                                    else:
                                        send_message(chat_id, "📦 У вас еще нет заказов")
                            
                            elif text == "ℹ️ Ma'lumotlar" or text == "ℹ️ Информация":
                                show_info(chat_id)
                            
                            elif text == "✍️ Fikr qoldirish" or text == "✍️ Оставить отзыв":
                                start_feedback(chat_id)
                            
                            elif text == "☎️ Bog'lanish" or text == "☎️ Контакты":
                                show_contacts(chat_id)
                            
                            elif text == "👑 Admin Panel" and str(chat_id) == ADMIN_ID:
                                today_orders = len([o for o in orders_data.values() if datetime.fromisoformat(o['timestamp']).date() == get_uzbekistan_time().date()])
                                admin_text = f"""
👑 <b>ADMIN PANELI</b>

📊 Bugungi buyurtmalar: {today_orders} ta
👥 Jami mijozlar: {len(user_data)} ta
💰 Jami buyurtmalar: {len(orders_data)} ta
🕒 Vaqt: {get_uzbekistan_time().strftime('%H:%M')}
"""
                                send_message(chat_id, admin_text)
                            
                            elif text == "🌍 Tilni o'zgartirish":
                                change_language(chat_id)
                            
                            elif text == "🏠 Asosiy menyu" or text == "🏠 Главное меню":
                                send_message(chat_id, "🏠 Asosiy menyu", main_menu_with_language(chat_id))
                            
                            # To'lov usullari
                            elif text == "💳 Karta orqali to'lash" or text == "💳 Оплата картой":
                                # Oxirgi buyurtmani topish
                                user_orders = [order_id for order_id, order in orders_data.items() if order["user_id"] == chat_id and order["status"] == "yangi"]
                                if user_orders:
                                    last_order_id = max(user_orders)
                                    orders_data[last_order_id]["payment_method"] = "karta"
                                    show_card_payment(chat_id, last_order_id)
                                    send_order_to_admin(last_order_id)
                                else:
                                    lang = user_language.get(chat_id, "uz")
                                    if lang == "uz":
                                        send_message(chat_id, "❌ Faol buyurtma topilmadi")
                                    else:
                                        send_message(chat_id, "❌ Активный заказ не найден")
                            
                            elif text == "💵 Naqd pul" or text == "💵 Наличные":
                                # Oxirgi buyurtmani topish
                                user_orders = [order_id for order_id, order in orders_data.items() if order["user_id"] == chat_id and order["status"] == "yangi"]
                                if user_orders:
                                    last_order_id = max(user_orders)
                                    orders_data[last_order_id]["payment_method"] = "naqd pul"
                                    confirm_cash_payment(chat_id, last_order_id)
                                    send_order_to_admin(last_order_id)
                                else:
                                    lang = user_language.get(chat_id, "uz")
                                    if lang == "uz":
                                        send_message(chat_id, "❌ Faol buyurtma topilmadi")
                                    else:
                                        send_message(chat_id, "❌ Активный заказ не найден")
                            
                            # Telefon qabul qilish
                            elif "contact" in message:
                                contact = message["contact"]
                                phone = contact.get("phone_number", "")
                                
                                if chat_id not in user_data:
                                    user_data[chat_id] = {}
                                user_data[chat_id]["phone"] = phone
                                lang = user_language.get(chat_id, "uz")
                                if lang == "uz":
                                    send_message(chat_id, f"✅ Telefon raqami qabul qilindi: {phone}")
                                else:
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
                                lang = user_language.get(chat_id, "uz")
                                if lang == "uz":
                                    send_message(chat_id, f"✅ Manzil qabul qilindi!\n📍 Google Maps")
                                else:
                                    send_message(chat_id, f"✅ Адрес принят!\n📍 Google Maps")
                                
                                # Buyurtma yaratish
                                create_order_from_cart(chat_id)
                            
                            # Yandex Maps linkini qabul qilish
                            elif text == "🌐 Yandex Maps havolasini yuborish" or text == "🌐 Отправить Yandex Maps ссылку":
                                lang = user_language.get(chat_id, "uz")
                                if lang == "uz":
                                    send_message(chat_id, "🌐 Iltimos, Yandex Maps havolangizni yuboring:")
                                else:
                                    send_message(chat_id, "🌐 Пожалуйста, отправьте вашу ссылку Yandex Maps:")
                            
                            # Xarita linklarini qabul qilish
                            elif "maps.google.com" in text or "goo.gl/maps" in text:
                                if chat_id not in user_data:
                                    user_data[chat_id] = {}
                                user_data[chat_id]["location"] = text
                                user_data[chat_id]["location_type"] = "google_maps"
                                lang = user_language.get(chat_id, "uz")
                                if lang == "uz":
                                    send_message(chat_id, f"✅ Google Maps manzili qabul qilindi!")
                                else:
                                    send_message(chat_id, f"✅ Адрес Google Maps принят!")
                                
                                # Buyurtma yaratish
                                create_order_from_cart(chat_id)
                            
                            elif "yandex" in text and "maps" in text:
                                if chat_id not in user_data:
                                    user_data[chat_id] = {}
                                user_data[chat_id]["location"] = text
                                user_data[chat_id]["location_type"] = "yandex_maps"
                                lang = user_language.get(chat_id, "uz")
                                if lang == "uz":
                                    send_message(chat_id, f"✅ Yandex Maps manzili qabul qilindi!")
                                else:
                                    send_message(chat_id, f"✅ Адрес Yandex Maps принят!")
                                
                                # Buyurtma yaratish
                                create_order_from_cart(chat_id)
                            
                            # Oddiy matn manzilni qabul qilish
                            elif text and len(text) > 10 and text not in ["🍽 Mazali Menyu", "🛒 Savat", "📦 Mening buyurtmalarim", "ℹ️ Ma'lumotlar", "✍️ Fikr qoldirish", "☎️ Bog'lanish", "👑 Admin Panel", "🏠 Asosiy menyu", "💳 Karta orqali to'lash", "💵 Naqd pul", "📍 Google Maps orqali", "🌐 Yandex Maps havolasini yuborish", "🍽 Вкусное Меню", "🛒 Корзина", "📦 Мои заказы", "ℹ️ Информация", "✍️ Оставить отзыв", "☎️ Контакты", "💳 Оплата картой", "💵 Наличные", "📍 Через Google Maps", "🌐 Отправить Yandex Maps ссылку"]:
                                if chat_id not in user_data:
                                    user_data[chat_id] = {}
                                user_data[chat_id]["location"] = text
                                user_data[chat_id]["location_type"] = "text"
                                lang = user_language.get(chat_id, "uz")
                                if lang == "uz":
                                    send_message(chat_id, f"✅ Manzil qabul qilindi!\n📍 {text}")
                                else:
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
