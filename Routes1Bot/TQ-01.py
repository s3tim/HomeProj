import telebot
from telebot import types

#ключ к боту
bot = telebot.TeleBot("7970047574:AAEL7j4lsTYbRzE4dYa7YEm2LYSzZh2o-Pg")

#города
cities = [
    {"n": "Москва", "a": True, "s": False},
    {"n": "Белгород", "a": True, "s": False},
    {"n": "Старый Оскол", "a": True, "s": False},
    {"n": "Губкин", "a": True, "s": False},
    {"n": "ГОРОД", "a": False, "s": False},
    {"n": "ГОРОД", "a": False, "s": False},
    {"n": "ГОРОД", "a": False, "s": False},
    {"n": "ГОРОД", "a": False, "s": False},
    {"n": "ГОРОД", "a": False, "s": False},
    {"n": "ГОРОД", "a": False, "s": False}
]

#нужно добавить город чтоб работало
routes = {
    "Москва": ["Маршрут 1", "Маршрут 2", "Маршрут 3", "Маршрут 4"],
    "Белгород": ["Маршрут 1", "Маршрут 2", "Маршрут 3", "Маршрут 4"],
    "Старый Оскол": ["Маршрут 1", "Маршрут 2", "Маршрут 3", "Маршрут 4"],
    "Губкин": ["Маршрут 1", "Маршрут 2", "Маршрут 3", "Маршрут 4"]
}

#city = {
#    "Москва": [""]
#}

#переход
NEXT = "загрузка локаций"

#ошибка
EROR = "Возникла ошибка, перезагрузите бота пожалуйста /start"

# Правила для_маршрутов 1
pr_Mockof_m1 = """Правила:
1. Соблюдайте скоростной режим
2. Не отклоняйтесь от маршрута
3. Следуйте указаниям гида"""
pr_Belgr_m1 = """Правила:
1. Соблюдайте скоростной режим
2. Не отклоняйтесь от маршрута
3. Следуйте указаниям гида"""
pr_Ctr_m1 = """Правила:
1. Соблюдайте скоростной режим
2. Не отклоняйтесь от маршрута
3. Следуйте указаниям гида"""
pr_Gubkin_m1 = """Правила:
1. Соблюдайте скоростной режим
2. Не отклоняйтесь от маршрута
3. Следуйте указаниям гида"""

# Правила для маршрутов 2
pr_Mockof_m2 = """Правила:
1. Соблюдайте скоростной режим
2. Не отклоняйтесь от маршрута
3. Следуйте указаниям гида"""
pr_Belgr_m2 = """Правила:
1. Соблюдайте скоростной режим
2. Не отклоняйтесь от маршрута
3. Следуйте указаниям гида"""
pr_Ctr_m2 = """Правила:
1. Соблюдайте скоростной режим
2. Не отклоняйтесь от маршрута
3. Следуйте указаниям гида"""
pr_Gubkin_m2 = """Правила:
1. Соблюдайте скоростной режим
2. Не отклоняйтесь от маршрута
3. Следуйте указаниям гида"""

# Правила для_маршрутов 3
pr_Mockof_m3 = """Правила:
1. Соблюдайте скоростной режим
2. Не отклоняйтесь от маршрута
3. Следуйте указаниям гида"""
pr_Belgr_m3 = """Правила:
1. Соблюдайте скоростной режим
2. Не отклоняйтесь от маршрута
3. Следуйте указаниям гида"""
pr_Ctr_m3 = """Правила:
1. Соблюдайте скоростной режим
2. Не отклоняйтесь от маршрута
3. Следуйте указаниям гида"""
pr_Gubkin_m3 = """Правила:
1. Соблюдайте скоростной режим
2. Не отклоняйтесь от маршрута
3. Следуйте указаниям гида"""

# Правила для_маршрутов 4
pr_Mockof_m4 = """Правила:
1. Соблюдайте скоростной режим
2. Не отклоняйтесь от маршрута
3. Следуйте указаниям гида"""
pr_Belgr_m4 = """Правила:
1. Соблюдайте скоростной режим
2. Не отклоняйтесь от маршрута
3. Следуйте указаниям гида"""
pr_Ctr_m4 = """Правила:
1. Соблюдайте скоростной режим
2. Не отклоняйтесь от маршрута
3. Следуйте указаниям гида"""
pr_Gubkin_m4 = """Правила:
1. Соблюдайте скоростной режим
2. Не отклоняйтесь от маршрута
3. Следуйте указаниям гида"""

STP30 = "none"        #это глобальная переменная для 3-4 шага привежи ее значение 
stp1 = False
stp2 = False
stp3 = False


@bot.message_handler(commands=["start"])
def step1(message):
    global stp1
    global stp2
    global stp3
    global STP30
    stp1 = False
    stp2 = False
    stp3 = False
    STP30 = "none"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    active_cities = [city["n"] for city in cities if city["a"]]   #список что-то типо city - "n" в cities фильтрация в "a"
    
    # по 2 кнопки на строку
    for i in range(0, len(active_cities), 2):
        row = [types.KeyboardButton(city) for city in active_cities[i:i+2]]
        markup.row(*row)
    
    bot.send_message(message.chat.id, "Выберите город:", reply_markup=markup)
    stp1 = True


    if city == "Москва" and route == routes["Москва"][0]:
        bot.send_message(message.chat.id, "Первый")

    if city == "Белгород" and route == routes["Белгород"][0]:
        bot.send_message(message.chat.id, "Первый")



@bot.message_handler(func=lambda message: message.text in routes.keys() and stp1)
def step2(message):
    city = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)    
    city_routes = routes.get(city, [])
    
    # кнопки маршрутов
    for i in range(0, len(city_routes), 3):
        row = [types.KeyboardButton(route) for route in city_routes[i:i+3]]
        markup.row(*row)
    bot.send_message(message.chat.id, f"Маршруты из города {city}:", reply_markup=markup)
    global stp2
    stp2 = True

@bot.message_handler(func=lambda message: stp2)
def step3(message):             
    quest = message.text
    global stp3, STP30                           

    #Маршруты 1
    if quest == routes["Москва"][0]:
        if not stp3:
            STP30 = "MOSKOV_1"
            markup = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(text=f"Начать {quest}", callback_data="route_0_start")
            markup.add(start_button)
            bot.send_message(chat_id=message.chat.id, text=pr_Mockof_m1, reply_markup=markup)
            stp3 = True
    elif quest == routes["Белгород"][0]:
            STP30 = "BELGOROD_1"
            markup = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(text=f"Начать {quest}", callback_data="route_0_start")
            markup.add(start_button)
            bot.send_message(chat_id=message.chat.id, text=pr_Belgr_m1, reply_markup=markup)
            stp3 = True
    elif quest == routes["Старый Оскол"][0]:
        if not stp3:
            STP30 = "STARY_OSKOL_1"
            markup = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(text=f"Начать {quest}", callback_data="route_0_start")
            markup.add(start_button)
            bot.send_message(chat_id=message.chat.id, text=pr_Ctr_m1, reply_markup=markup)
            stp3 = True
    elif quest == routes["Губкин"][0]:
        if not stp3:
            STP30 = "GUBKIN_1"
            markup = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(text=f"Начать {quest}", callback_data="route_0_start")
            markup.add(start_button)
            bot.send_message(chat_id=message.chat.id, text=pr_Gubkin_m1, reply_markup=markup)
            stp3 = True
            
    #Маршруты 2
    elif quest == routes["Москва"][1]:
        if not stp3:
            STP30 = "MOSKOV_2"
            markup = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(text=f"Начать {quest}", callback_data="route_0_start")
            markup.add(start_button)
            bot.send_message(chat_id=message.chat.id, text=pr_Mockof_m2, reply_markup=markup)
            stp3 = True
    elif quest == routes["Белгород"][1]:
        if not stp3:
            STP30 = "BELGOROD_2"
            markup = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(text=f"Начать {quest}", callback_data="route_0_start")
            markup.add(start_button)
            bot.send_message(chat_id=message.chat.id, text=pr_Belgr_m2, reply_markup=markup)
            stp3 = True
    elif quest == routes["Старый Оскол"][1]:
        if not stp3:
            STP30 = "STARY_OSKOL_2"
            markup = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(text=f"Начать {quest}", callback_data="route_0_start")
            markup.add(start_button)
            bot.send_message(chat_id=message.chat.id, text=pr_Ctr_m2, reply_markup=markup)
            stp3 = True
    elif quest == routes["Губкин"][1]:
        if not stp3:
            STP30 = "GUBKIN_2"
            markup = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(text=f"Начать {quest}", callback_data="route_0_start")
            markup.add(start_button)
            bot.send_message(chat_id=message.chat.id, text=pr_Gubkin_m2, reply_markup=markup)
            stp3 = True
            
    #Маршруты 3
    elif quest == routes["Москва"][2]:
        if not stp3:
            STP30 = "MOSKOV_3"
            markup = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(text=f"Начать {quest}", callback_data="route_0_start")
            markup.add(start_button)
            bot.send_message(chat_id=message.chat.id, text=pr_Mockof_m3, reply_markup=markup)
            stp3 = True
    elif quest == routes["Белгород"][2]:
        if not stp3:
            STP30 = "BELGOROD_3"
            markup = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(text=f"Начать {quest}", callback_data="route_0_start")
            markup.add(start_button)
            bot.send_message(chat_id=message.chat.id, text=pr_Belgr_m3, reply_markup=markup)
            stp3 = True
    elif quest == routes["Старый Оскол"][2]:
        if not stp3:
            STP30 = "STARY_OSKOL_3"
            markup = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(text=f"Начать {quest}", callback_data="route_0_start")
            markup.add(start_button)
            bot.send_message(chat_id=message.chat.id, text=pr_Ctr_m3, reply_markup=markup)
            stp3 = True
    elif quest == routes["Губкин"][2]:
        if not stp3:
            STP30 = "GUBKIN_3"
            markup = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(text=f"Начать {quest}", callback_data="route_0_start")
            markup.add(start_button)
            bot.send_message(chat_id=message.chat.id, text=pr_Gubkin_m3, reply_markup=markup)
            stp3 = True
    
    #Маршруты 4
    elif quest == routes["Москва"][3]:
        if not stp3:
            STP30 = "MOSKOV_4"
            markup = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(text=f"Начать {quest}", callback_data="route_0_start")
            markup.add(start_button)
            bot.send_message(chat_id=message.chat.id, text=pr_Mockof_m4, reply_markup=markup)
            stp3 = True
    elif quest == routes["Белгород"][3]:
        if not stp3:
            STP30 = "BELGOROD_4"
            markup = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(text=f"Начать {quest}", callback_data="route_0_start")
            markup.add(start_button)
            bot.send_message(chat_id=message.chat.id, text=pr_Belgr_m4, reply_markup=markup)
            stp3 = True
    elif quest == routes["Старый Оскол"][3]:
        if not stp3:
            STP30 = "STARY_OSKOL_4"
            markup = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(text=f"Начать {quest}", callback_data="route_0_start")
            markup.add(start_button)
            bot.send_message(chat_id=message.chat.id, text=pr_Ctr_m4, reply_markup=markup)
            stp3 = True
    elif quest == routes["Губкин"][3]:
        if not stp3:
            STP30 = "GUBKIN_4"
            markup = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(text=f"Начать {quest}", callback_data="route_0_start")
            markup.add(start_button)
            bot.send_message(chat_id=message.chat.id, text=pr_Gubkin_m4, reply_markup=markup)
            stp3 = True

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global stp3, EROR

    if callback.data == "route_0_start":
        for i in range(0, 6):
            try:
                bot.delete_message(callback.message.chat.id, callback.message.message_id - i)
            except:
                print(EROR)
    
    sent_msg = bot.send_message(callback.message.chat.id, NEXT)

    class FakeMessage:                  #вызываем step4
        def __init__(self):
            self.chat = callback.message.chat                
            self.text = NEXT
            self.message_id = sent_msg.message_id
    step4(FakeMessage())

@bot.message_handler(func=lambda message: stp3 and message.text == NEXT)
def step4(message): 
    global stp3, STP30
    if STP30 == "none":
        bot.send_message(message.chat.id, "Ошибка: маршрут не выбран")
    else:
        bot.send_message(message.chat.id, STP30)
    stp3 = False  

    #надо вывести STP30 на step4 и добавить его в step3 правильно

bot.infinity_polling()
