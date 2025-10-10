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

# TO'LIQ MENYU MA'LUMOTLARI - BARCHA RASMLAR BILAN
menu_data = {
    "holodnye_rolly": {
        "name": "🍣 ХОЛОДНЫЕ РОЛЛЫ",
        "emoji": "🍣",
        "products": [
            {"id": 1, "name": "Филадельфия Голд", "price": 120000, "description": "Сыр.Лосось.Огурец.Угорь.Унаги соус.Тунец.Кунжут.Массаго икра", "prep_time": "20 daqiqa", "image": "https://i.ibb.co/GQC6b0Jx/filadelfiya-gold.jpg"},
            {"id": 2, "name": "Филадельфия (Тунец)", "price": 90000, "description": "Сыр.Тунец", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/LzWDsSLL/filadelfiya-tunets.jpg"},
            {"id": 3, "name": "Филадельфия Классик", "price": 80000, "description": "Сыр.Огурецы.Лосось", "prep_time": "12 daqiqa", "image": "https://i.ibb.co/x8mtrwnr/filadelfiya-classic.jpg"},
            {"id": 4, "name": "Эби Голд", "price": 110000, "description": "Сыр.Лосось.Креветки в кляре.Огурец.Лук", "prep_time": "18 daqiqa", "image": "https://i.ibb.co/ymzTLB2d/ebi-gold.jpg"},
            {"id": 5, "name": "Лосось (гриль)", "price": 93000, "description": "Сыр.Унаги соус.Лосось.Массаго", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/qMwVCNkJ/losos-grill.jpg"},
            {"id": 6, "name": "Калифорния с креветками", "price": 80000, "description": "Сыр.Огурец.Креветки тигровые.Массаго красс", "prep_time": "12 daqiqa", "image": "https://i.ibb.co/npfwvNQ/california-krevetka.jpg"},
            {"id": 7, "name": "Калифорния с лососем", "price": 76000, "description": "Сыр.Огурец.Лосось.Массаго красс", "prep_time": "12 daqiqa", "image": "https://i.ibb.co/ZRX11xwV/california-losos.jpg"},
            {"id": 8, "name": "Калифорния с крабом", "price": 70000, "description": "Сыр.Огурец.Снежный краб.Массаго красный", "prep_time": "12 daqiqa", "image": "https://i.ibb.co/cXNm1Lws/california-krab.jpg"},
            {"id": 9, "name": "Ролл Огурец", "price": 65000, "description": "Сыр.Стружка тунца.Огурец", "prep_time": "10 daqiqa", "image": "https://i.ibb.co/gLGNmQNL/roll-ogurec.jpg"},
            {"id": 91, "name": "Ролл в Кунжуте", "price": 50000, "description": "Сыр.Кунжут.Краб", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/MxFj5fc9/roll-kunjut.jpg"},
            {"id": 92, "name": "Дракон", "price": 75000, "description": "Сыр.Угорь.Огурец", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/TBMTxXkK/drakon.jpg"},
            {"id": 93, "name": "Канада GOLD", "price": 85000, "description": "Сыр.Лосось.Огурец.Угорь.Унаги соус.Кунжут", "prep_time": "20 daqiqa", "image": "https://i.ibb.co/Q7tpSZRW/kanada-gold.jpg"}
        ]
    },
    "zapechennye": {
        "name": "🔥 ЗАПЕЧЕННЫЕ",
        "emoji": "🔥",
        "products": [
            {"id": 10, "name": "Ролл Филадельфия Стейк", "price": 95000, "description": "Сыр.лосось.огурец.сырная шапка", "prep_time": "18 daqiqa", "image": "https://i.ibb.co/C5qhrcSR/roll-filadelfiya-steak.jpg"},
            {"id": 11, "name": "Ролл с креветкой", "price": 80000, "description": "Сыр.Тигровые креветки.сырная шапка.Огурец.кунжут", "prep_time": "16 daqiqa", "image": "https://i.ibb.co/V03yy7Jy/roll-krevetka.jpg"},
            {"id": 12, "name": "Ролл с угрем", "price": 80000, "description": "Сыр.огурецы.кунжут.сырная шапка.угорь", "prep_time": "16 daqiqa", "image": "https://i.ibb.co/TD83xGMz/roll-ugor.jpg"},
            {"id": 13, "name": "Ролл с крабом", "price": 66000, "description": "Сыр.Огурец.Снежный краб", "prep_time": "14 daqiqa", "image": "https://i.ibb.co/Zzn5hb1c/roll-krab.jpg"},
            {"id": 14, "name": "Ролл с лососем", "price": 77000, "description": "Сыр.Огурецы.кунжут,сырная шапка,лосось,унаги соус", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/VZkcJx2/roll-losos.jpg"},
            {"id": 15, "name": "Ролл Калифорния", "price": 70000, "description": "Сыр.Огурецы.снежный краб.икра массаго.сырная шапка.унаги соус", "prep_time": "14 daqiqa", "image": "https://i.ibb.co/XfGFW7Ss/roll-california.jpg"},
            {"id": 16, "name": "Ролл с курицей", "price": 55000, "description": "Майонез.Салат Айзберг.курица.сырная шапка", "prep_time": "12 daqiqa", "image": "https://i.ibb.co/zWPhtZ2m/roll-kurica.jpg"},
            {"id": 94, "name": "Лосось", "price": 66000, "description": "Лосось, Кунжут", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/MxzTgnLD/losos.jpg"},
            {"id": 95, "name": "Темпура с крабом", "price": 55000, "description": "Краб.Мойонез.Унаги соус", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/1JRBHPQj/tempura-krab.jpg"},
            {"id": 96, "name": "Креветки", "price": 70000, "description": "Креветки, сырная шапка", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/d4QM7zfJ/krevetki.jpg"},
            {"id": 97, "name": "Темпура запеченный", "price": 70000, "description": "Сыр.Краб.Огурец", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/QFjbcnG9/tempura-zapechenny.jpg"}
        ]
    },
    "jarennye_rolly": {
        "name": "⚡ ЖАРЕНЫЕ РОЛЛЫ",
        "emoji": "⚡",
        "products": [
            {"id": 17, "name": "Темпура (Тунец)", "price": 75000, "description": "Огурец.Сыр.Тунец", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/qQJVGwz/tempura-tunets.jpg"},
            {"id": 18, "name": "Темпура Угорь", "price": 71000, "description": "Сыр.Огурец.Угорь.Массаго красс.Унаги соус", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/bj64nKKm/tempura-ugor.jpg"},
            {"id": 19, "name": "Темпура с креветками", "price": 70000, "description": "Сыр.Огурец.Креветки тигровые.Массаго красс.Унаги соус", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/CKC4dXxm/tempura-krevetki.jpg"},
            {"id": 20, "name": "Темпура с лососем", "price": 66000, "description": "Сыр.Огурец.Лосось.Унаги соус.Кунжут", "prep_time": "14 daqiqa", "image": "https://i.ibb.co/DfnTqrM8/tempura-losos.jpg"},
            {"id": 21, "name": "Темпура Курица", "price": 48000, "description": "Айсберг.Майонез.Курица.Унаги соус", "prep_time": "12 daqiqa", "image": "https://i.ibb.co/mF8yM6TC/tempura-kurica.jpg"},
            {"id": 98, "name": "Ясареные роялы", "price": 71000, "description": "Запеченные роллы с унаги соусом", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/JWN5qYyb/yasarenie-royaly.jpg"}
        ]
    },
    "sety": {
        "name": "🎎 СЕТЫ",
        "emoji": "🎎",
        "products": [
            {"id": 22, "name": "Сет Токио 48шт", "price": 390000, "description": "Дракон ролл 8шт + Филадельфия классик 8шт + Темпура Лосось 8шт + Краб Запеченый 16шт + Калифорния Лосось 8шт", "prep_time": "40 daqiqa", "image": "https://i.ibb.co/8Dkf54z0/set-tokio.jpg"},
            {"id": 23, "name": "Сет Ямамото 32шт", "price": 290000, "description": "Филадельфия классик 8шт + Калифорния классик 8шт + Ролл с креветками 8шт + Ролл Чука 8шт", "prep_time": "35 daqiqa", "image": "https://i.ibb.co/DPpPLQgg/set-yamamoto.jpg"},
            {"id": 24, "name": "Сет Идеал 32шт", "price": 260000, "description": "Филадельфия классик 8шт + Калифорния Кунсут 8шт + Калифорния Черный 8шт + Дракон ролл 8шт", "prep_time": "32 daqiqa", "image": "https://i.ibb.co/gZpQSSzf/set-ideal.jpg"},
            {"id": 25, "name": "Сет Окей 24шт", "price": 200000, "description": "Филадельфия классик 8шт + Запеченый лосось 8шт + Темпура лосось 8шт", "prep_time": "30 daqiqa", "image": "https://i.ibb.co/sdBH78W4/set-okey.jpg"},
            {"id": 26, "name": "Сет Сакура 24шт", "price": 180000, "description": "Филадельфия классик 4шт + Канада Голд 4шт + Мини ролл лосось 8шт + Темпура лосось 8шт", "prep_time": "28 daqiqa", "image": "https://i.ibb.co/dNZyGMn/set-sakura.jpg"},
            {"id": 27, "name": "Сет Классический 32шт", "price": 150000, "description": "Мини ролл лосось 8шт + Мини ролл огурец 8шт + Мини ролл тунец 8шт + Мини ролл краб 8шт", "prep_time": "25 daqiqa", "image": "https://i.ibb.co/fVjKB1vS/set-klassicheskiy.jpg"}
        ]
    },
    "sushi_gunkan": {
        "name": "🍱 СУШИ И ГУНКАН",
        "emoji": "🍱",
        "products": [
            {"id": 28, "name": "Гункан Тунец", "price": 30000, "description": "Tunetsli gunkan", "prep_time": "5 daqiqa", "image": "https://i.ibb.co/JWYVRq3Z/gunkan-tunets.jpg"},
            {"id": 29, "name": "Суши Тунец", "price": 25000, "description": "Tunetsli sushi", "prep_time": "5 daqiqa", "image": "https://i.ibb.co/yck5fm10/sushi-tunets.jpg"},
            {"id": 30, "name": "Мини Тунец", "price": 34000, "description": "Mini tunets sushi", "prep_time": "5 daqiqa", "image": "https://i.ibb.co/VpSTV2jZ/mini-tunets.jpg"},
            {"id": 31, "name": "Гункан Лосось", "price": 24000, "description": "Lososli gunkan", "prep_time": "5 daqiqa", "image": "https://i.ibb.co/wZ8cHQ3B/gunkan-losos.jpg"},
            {"id": 32, "name": "Суши Лосось", "price": 20000, "description": "Lososli sushi", "prep_time": "5 daqiqa", "image": "https://i.ibb.co/3ycXwTn3/sushi-losos.jpg"},
            {"id": 33, "name": "Мини Лосось", "price": 34000, "description": "Mini losos sushi", "prep_time": "5 daqiqa", "image": "https://i.ibb.co/bMnZDM8v/mini-losos.jpg"},
            {"id": 34, "name": "Гункан Угорь", "price": 24000, "description": "Ugorli gunkan", "prep_time": "5 daqiqa", "image": "https://i.ibb.co/FLrCy969/gunkan-ugor.jpg"},
            {"id": 35, "name": "Суши Угорь", "price": 23000, "description": "Ugorli sushi", "prep_time": "5 daqiqa", "image": "https://i.ibb.co/Q3B6yMxV/sushi-ugor.jpg"},
            {"id": 36, "name": "Мини Угорь", "price": 34000, "description": "Mini ugor sushi", "prep_time": "5 daqiqa", "image": "https://i.ibb.co/YFfW3pFJ/mini-ugor.jpg"},
            {"id": 37, "name": "Гункан Массаго", "price": 24000, "description": "Massago gunkan", "prep_time": "5 daqiqa", "image": "https://i.ibb.co/DHsDJyTf/gunkan-massago.jpg"},
            {"id": 38, "name": "Суши Креветка", "price": 20000, "description": "Qisqichbaqali sushi", "prep_time": "5 daqiqa", "image": "https://i.ibb.co/rfbG3L2h/sushi-krevetka.jpg"},
            {"id": 39, "name": "Мини Краб", "price": 23000, "description": "Mini krab sushi", "prep_time": "5 daqiqa", "image": "https://i.ibb.co/Xx1ghHBw/mini-krab.jpg"},
            {"id": 40, "name": "Мини Огурец", "price": 15000, "description": "Mini bodring sushi", "prep_time": "5 daqiqa", "image": "https://i.ibb.co/HT83N6gt/mini-ogurec.jpg"}
        ]
    },
    "goryachaya_eda": {
        "name": "🍜 ГОРЯЧАЯ ЕДА",
        "emoji": "🍜",
        "products": [
            {"id": 41, "name": "Рамэн Классик", "price": 80000, "description": "An'anaviy yapon rameni", "prep_time": "20 daqiqa", "image": "https://i.ibb.co/p6SdB15J/ramen-classic.jpg"},
            {"id": 42, "name": "Рамэн Токио", "price": 66000, "description": "Maxsus ramen", "prep_time": "25 daqiqa", "image": "https://i.ibb.co/Q3dFbp3X/ramen-tokio.jpg"},
            {"id": 43, "name": "Вок с говядиной", "price": 65000, "description": "Mol go'shti bilan vok", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/4nrmxLW2/vok-govyadina.jpg"},
            {"id": 44, "name": "Том Ям Токио", "price": 95000, "description": "Taylandcha Tom Yam", "prep_time": "30 daqiqa", "image": "https://i.ibb.co/5xYJbRfc/tom-yam-tokio.jpg"},
            {"id": 45, "name": "Куриные крылышки", "price": 35000, "description": "Qovurilgan tovuq qanotchalar", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/k20FYLZs/kurinye-krylyshki.jpg"},
            {"id": 46, "name": "Кукси", "price": 40000, "description": "Koreyscha kuksi", "prep_time": "10 daqiqa", "image": "https://i.ibb.co/57sXdTZ/kuksi.jpg"},
            {"id": 47, "name": "Вок с курицей", "price": 55000, "description": "Tovuqli vok", "prep_time": "12 daqiqa", "image": "https://i.ibb.co/VZCZTrp/vok-kurica.jpg"},
            {"id": 48, "name": "Том Ям Классик", "price": 70000, "description": "Oddiy Tom Yam", "prep_time": "25 daqiqa", "image": "https://i.ibb.co/tP8T9WVg/tom-yam-classic.jpg"},
            {"id": 49, "name": "Хрустящие баклажаны", "price": 45000, "description": "Qarsildoq baqlajonlar", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/b5jt6yRR/hrustyaschie-baklazhany.jpg"},
            {"id": 50, "name": "Цезарь с курицей", "price": 45000, "description": "Sezar salati", "prep_time": "10 daqiqa", "image": "https://i.ibb.co/Nd38hmJQ/cezar-kurica.jpg"},
            {"id": 51, "name": "Греческий салат", "price": 50000, "description": "Rukola bilan salat", "prep_time": "8 daqiqa", "image": "https://i.ibb.co/B5NY9D39/grecheskiy-salat.jpg"},
            {"id": 52, "name": "Салат Руккола", "price": 40000, "description": "Rukola salati", "prep_time": "8 daqiqa", "image": "https://i.ibb.co/5xsnpW3c/salat-rukkola.jpg"},
            {"id": 53, "name": "Мужской Каприз", "price": 40000, "description": "Kapriz salati", "prep_time": "8 daqiqa", "image": "https://i.ibb.co/HDC28VSN/muzhskoy-kapriz.jpg"},
            {"id": 54, "name": "Чука Салат", "price": 35000, "description": "Fuka salati", "prep_time": "8 daqiqa", "image": "https://i.ibb.co/TDh7Bz76/chuka-salat.jpg"},
            {"id": 55, "name": "Тар-Тар", "price": 15000, "description": "Tar-Tar sousi bilan", "prep_time": "5 daqiqa", "image": "https://i.ibb.co/zTJMDKQH/tar-tar.jpg"},
            {"id": 56, "name": "Рамэн", "price": 45000, "description": "Oddiy ramen", "prep_time": "18 daqiqa", "image": "https://i.ibb.co/QFZZTtp2/ramen.jpg"}
        ]
    },
    "pizza_burger": {
        "name": "🍕 ПИЦЦА И БУРГЕР",
        "emoji": "🍕",
        "products": [
            {"id": 57, "name": "Токио Микс 35см", "price": 90000, "description": "Tokio miks pizza 35sm", "prep_time": "25 daqiqa", "image": "https://i.ibb.co/7th0vwxT/tokio-miks-pizza.jpg"},
            {"id": 58, "name": "Кази 35см", "price": 90000, "description": "Bazi pizza 35sm", "prep_time": "25 daqiqa", "image": "https://i.ibb.co/bMYmp7Kq/kazi-pizza.jpg"},
            {"id": 59, "name": "Микс 35см", "price": 85000, "description": "Aralash pizza 35sm", "prep_time": "22 daqiqa", "image": "https://i.ibb.co/jksjJ4Jt/miks-pizza.jpg"},
            {"id": 60, "name": "Пепперони 35см", "price": 80000, "description": "Pishloqli pizza 35sm", "prep_time": "20 daqiqa", "image": "https://i.ibb.co/VWx6vgQK/pepperoni-pizza.jpg"},
            {"id": 61, "name": "Кузикорин 35см", "price": 80000, "description": "Kuzidirini pizza 35sm", "prep_time": "20 daqiqa", "image": "https://i.ibb.co/LhnynQdb/kuzikorin-pizza.jpg"},
            {"id": 62, "name": "Маргарита 35см", "price": 75000, "description": "Margarita pizza 35sm", "prep_time": "18 daqiqa", "image": "https://i.ibb.co/gMXHywj0/margarita-pizza.jpg"},
            {"id": 63, "name": "Гамбургер", "price": 28000, "description": "Gamburger", "prep_time": "10 daqiqa", "image": "https://i.ibb.co/hJWnm5ct/gamburger.jpg"},
            {"id": 64, "name": "Чизбургер", "price": 33000, "description": "Chizburger", "prep_time": "12 daqiqa", "image": "https://i.ibb.co/NBChXQN/chizburger.jpg"},
            {"id": 65, "name": "Токио Бургер", "price": 37000, "description": "Tokio maxsus burger", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/4Z8SY79y/tokio-burger.jpg"},
            {"id": 66, "name": "Куриные крылышки", "price": 35000, "description": "Qovurilgan tovuq qanotchalar", "prep_time": "15 daqiqa", "image": "https://i.ibb.co/k20FYLZs/kurinye-krylyshki.jpg"},
            {"id": 67, "name": "Сырные шарики", "price": 22000, "description": "Pishloq shariklari", "prep_time": "8 daqiqa", "image": "https://i.ibb.co/57sXdTZ/syrnye-shariki.jpg"},
            {"id": 68, "name": "Картофель Фри", "price": 22000, "description": "Qovurilgan kartoshka", "prep_time": "7 daqiqa", "image": "https://i.ibb.co/VZCZTrp/kartofel-fri.jpg"},
            {"id": 69, "name": "Клаб Сендвич", "price": 35000, "description": "Klub sendvich", "prep_time": "10 daqiqa", "image": "https://i.ibb.co/tP8T9WVg/klab-sendvich.jpg"}
        ]
    },
    "napitki": {
        "name": "🥤 НАПИТКИ",
        "emoji": "🥤",
        "products": [
            {"id": 70, "name": "Мохито 1л", "price": 45000, "description": "Sovuq mojito", "prep_time": "3 daqiqa", "image": ""},
            {"id": 71, "name": "Мохито 0.7л", "price": 25000, "description": "Sovuq mojito", "prep_time": "3 daqiqa", "image": ""},
            {"id": 72, "name": "Мохито 0.5л", "price": 20000, "description": "Sovuq mojito", "prep_time": "3 daqiqa", "image": ""},
            {"id": 73, "name": "Чай Чудо", "price": 35000, "description": "Maxsus choy", "prep_time": "2 daqiqa", "image": ""},
            {"id": 74, "name": "Чай Токио", "price": 35000, "description": "Tokio maxsus choy", "prep_time": "2 daqiqa", "image": ""},
            {"id": 75, "name": "Чай Фруктовый", "price": 35000, "description": "Mevali choy", "prep_time": "2 daqiqa", "image": ""},
            {"id": 76, "name": "Чай Тархун", "price": 35000, "description": "Tarxun choyi", "prep_time": "2 daqiqa", "image": ""},
            {"id": 77, "name": "Чай Багини", "price": 35000, "description": "Rayhon choyi", "prep_time": "2 daqiqa", "image": ""},
            {"id": 78, "name": "Чай Каркаде", "price": 30000, "description": "Karkade choyi", "prep_time": "2 daqiqa", "image": ""},
            {"id": 79, "name": "Чай Лимон", "price": 25000, "description": "Limonli choy", "prep_time": "2 daqiqa", "image": ""},
            {"id": 80, "name": "Милкшейк Клубника", "price": 30000, "description": "Qulupnayli milkshake", "prep_time": "5 daqiqa", "image": ""},
            {"id": 81, "name": "Милкшейк Сникерс", "price": 30000, "description": "Snickers milkshake", "prep_time": "5 daqiqa", "image": ""},
            {"id": 82, "name": "Милкшейк Банан", "price": 30000, "description": "Bananli milkshake", "prep_time": "5 daqiqa", "image": ""},
            {"id": 83, "name": "Милкшейк Орео", "price": 30000, "description": "Oreo milkshake", "prep_time": "5 daqiqa", "image": ""},
            {"id": 84, "name": "Милкшейк Киви", "price": 30000, "description": "Kinder milkshake", "prep_time": "5 daqiqa", "image": ""},
            {"id": 85, "name": "Кола 1л", "price": 14000, "description": "Gazlangan ichimlik 1L", "prep_time": "1 daqiqa", "image": ""},
            {"id": 86, "name": "Фанта 1л", "price": 14000, "description": "Gazlangan ichimlik 1L", "prep_time": "1 daqiqa", "image": ""},
            {"id": 87, "name": "Фюсти 1л", "price": 13000, "description": "Gazlangan ichimlik 1L", "prep_time": "1 daqiqa", "image": ""},
            {"id": 88, "name": "Кола-Фанта Ж/Б", "price": 10000, "description": "Kola 0.5L", "prep_time": "1 daqiqa", "image": ""},
            {"id": 89, "name": "Вода Без Газа", "price": 8000, "description": "Gazsiz suv", "prep_time": "1 daqiqa", "image": ""},
            {"id": 90, "name": "Сок", "price": 19000, "description": "Tabiiy sok", "prep_time": "1 daqiqa", "image": ""}
        ]
    }
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
        # Agar rasm yuborishda xato bo'lsa, oddiy xabar yuboramiz
        if caption:
            send_message(chat_id, caption, keyboard)
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

# ==================== MAVJUD FUNKSIYALAR ====================

def get_uzbekistan_time():
    return datetime.utcnow() + timedelta(hours=5)

def send_message(chat_id, text, keyboard=None):
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
    
    if chat_id not in user_data:
        user_data[chat_id] = {"cart": []}
    
    if "cart" not in user_data[chat_id]:
        user_data[chat_id]["cart"] = []
    
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
    if chat_id not in user_data or "cart" not in user_data[chat_id] or not user_data[chat_id]["cart"]:
        send_message(chat_id, "🛒 <b>Ваша корзина пуста</b>\n\nПожалуйста, выберите продукты из меню!")
        return
    
    cart = user_data[chat_id]["cart"]
    total = sum(item['price'] for item in cart)
    
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
            
        # ... qolgan callback handlerlar
    except Exception as e:
        print(f"Ошибка callback: {e}")
        send_message(chat_id, "❌ Произошла ошибка. Пожалуйста, попробуйте снова.")

# ... qolgan funksiyalar o'zgarmagan

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
