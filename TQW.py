import telebot
from telebot import types
import time

bot = telebot.TeleBot("7970047574:AAEL7j4lsTYbRzE4dYa7YEm2LYSzZh2o-Pg")

# Данные о городах
cities = [
    {"n": "Москва", "a": True, "s": False},
    {"n": "Белгород", "a": True, "s": False},
    {"n": "Старый Оскол", "a": True, "s": False},
    {"n": "Губкин", "a": True, "s": False}
]

# Маршруты для каждого города
routes = {
    "Москва": ["Маршрут 1", "Маршрут 2", "Маршрут 3", "Маршрут 4"],
    "Белгород": ["Маршрут 1", "Маршрут 2", "Маршрут 3", "Маршрут 4"],
    "Старый Оскол": ["Маршрут 1", "Маршрут 2", "Маршрут 3", "Маршрут 4"],
    "Губкин": ["Маршрут 1", "Маршрут 2", "Маршрут 3", "Маршрут 4"]
}

#База данных для маршрутов
        #маршруты НЕ МЕНЯТЬ
route_locations = {
    "Москва": {
        "Маршрут 1": ["Кремль", "Парк Горького", "Красная площадь"],
        "Маршрут 2": ["ВДНХ", "Останкинская башня"],
        # еще маршруты
    },
    "Белгород": {
        "Маршрут 1": ["Парк Победы", "Музей-диорама"],
        "Маршрут 2": ["Соборная площадь"],
    },
    "Старый Оскол": {
        "Маршрут 1": ["Кремль", "Парк Горького", "Красная площадь"],
        "Маршрут 2": ["ВДНХ", "Останкинская башня"],
    },
    "Губкин": {
        "Маршрут 1": ["Кремль", "Парк Горького", "Красная площадь"],
        "Маршрут 2": ["ВДНХ", "Останкинская башня"],
    }
}

# Текст правил для маршрутов
rules = {
    ("Москва", 1): "Правила Москва Маршрут 1:\n1. Правило 1\n2. Правило 2\n3. Правило 3",
    ("Москва", 2): "Правила Москва Маршрут 2:\n1. Правило 1\n2. Правило 2\n3. Правило 3",
    # Добавить остальное
}

# Состояние бота
current_state = {
    "city": None,
    "route": None,
    "step0": True,
    "step1": False,
    "step2": False,
    "step3": False,
    "step4": False,
    "step5": False
}
#В поддержке кто сылка
support_chell = "https://t.me/helpikChell"

PRIBET = "Привет, меня зовут ТимКвест. Я умная платформа.."
NEXT = "Загрузка локаций"
ERROR = "Ошибка, пожалуйста начните снова /start"
HELPIK = "Техподдержкой можно пользоваться если:\nВашего города нет в списке, вы можете связаться с нами удобным вам способом"

MOSKOV = "Первая локацияM"
BELGOROD = "Первая локацияB"
STARY_OSKOL = "Первая локацияS"
GUBKIN = "Первая локацияG"

@bot.callback_query_handler(func=lambda call: call.data == "send_start")
def callback_start(call):
    for i in range(10):
        bot.delete_message(call.message.chat.id, call.message.message_id - i)

    current_state.update({
        "city": None,
        "route": None,
        "step0": True,
        "step1": False,
        "step2": False,
        "step3": False,
        "step4": False,
        "step5": False
    })

@bot.message_handler(commands=["start"] or current_state["step0"])
def step1(message):
    current_state.update({
        "city": None,
        "route": None,
        "step0": True,
        "step1": True,
        "step2": False,
        "step3": False,
        "step4": False,
        "step5": False
    })

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    active_cities = [city["n"] for city in cities if city.get("a", False)]

    markup.add(*[types.KeyboardButton(city) for city in active_cities])
    markup.row(types.KeyboardButton("Техподдержка"))

    bot.send_message(message.chat.id, PRIBET)
    bot.send_message(message.chat.id, "Выберите город:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Техподдержка" or message.text == "/help")
def helpik(message):
    support_markup = types.InlineKeyboardMarkup()
    support_markup.add(
        types.InlineKeyboardButton(
            "Написать в поддержку",
            url="https://t.me/helpikChell"
        )
    )
    bot.send_message(
        message.chat.id,
        HELPIK,
        reply_markup=support_markup
    )

@bot.message_handler(func=lambda message: current_state["step1"] and message.text in routes.keys())
def step2(message):
    current_state.update({
        "city": message.text,
        "route": None,
        "step0": False,
        "step1": False,
        "step2": True,
        "step3": False,
        "step4": False,
        "step5": False
    })

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    city_routes = routes[message.text]

    for i in range(0, len(city_routes), 3):
        row = city_routes[i:i+3]
        markup.row(*row)

    bot.send_message(message.chat.id, f"Маршруты из города {message.text}:", reply_markup=markup)

@bot.message_handler(func=lambda message: current_state["step2"])
def step3(message):
    city = current_state["city"]
    if message.text not in routes[city]:
        bot.send_message(message.chat.id, "Пожалуйста, выберите маршрут из списка")
        return

    current_state.update({
        "route": message.text,
        "step0": False,
        "step1": False,
        "step2": False,
        "step3": True,
        "step4": False,
        "step5": False
    })

    route_n = routes[city].index(message.text) + 1
    rule_text = rules.get((city, route_n), "Правила для этого маршрута не указаны")

    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text=f"Начать {message.text}", callback_data="start_route")
    markup.add(start_button)
    reply_markup=types.ReplyKeyboardRemove()

    bot.send_message(message.chat.id, rule_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "start_route")
def handle_callback(call):
    for i in range(6):
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id - i)
        except:
            support_markup = types.InlineKeyboardMarkup()
            support_markup.add(
            types.InlineKeyboardButton(
            ERROR,
            url="https://t.me/helpikChell"
        )
    )
    bot.send_message(call.message.chat.id, NEXT)
    step4(call.message)

@bot.message_handler(func=lambda message: current_state["step3"] and message.text == NEXT) #разберись
def step4(message):
    city = current_state["city"]
    route = current_state["route"]
    is_active = any(c["n"] == city and c["a"] for c in cities)

    if city in routes:
        try:
            route_index = routes[city].index(route)
            if current_state ["step0"] == False:
                time.sleep(1)
                bot.send_message(message.chat.id, "3")
            if current_state ["step0"] == False:
                time.sleep(1)
                bot.send_message(message.chat.id, "2")
            if current_state ["step0"] == False:
                time.sleep(1)
                bot.send_message(message.chat.id, "1")
            if current_state ["step0"] == False:
                time.sleep(1)
                msg = bot.send_message(message.chat.id, f"{city}, {route} активирован")
        except ValueError:
            support_markup = types.InlineKeyboardMarkup()
            helpb = types.InlineKeyboardButton("Написать в поддержку", url="https://t.me/helpikChell")
            startb = types.InlineKeyboardButton("Начать все сначала(", callback_data="send_start")
            support_markup.row(helpb, startb)
            bot.send_message(
                message.chat.id,
                HELPIK,
                reply_markup=support_markup
            )
            current_state.update({
                "step0": True,
                "step1": False,
                "step2": False,
                "step3": False,
                "step4": False,
                "step5": False
            })


    current_state.update({
        "step0": False,
        "step1": False,
        "step2": False,
        "step3": False,
        "step4": True,
        "step5": False
    })
    step5(msg)

@bot.message_handler(func=lambda message: current_state["step4"] and message.text == current_state["city"])
def step5(message):
    city = current_state["city"]
    route = current_state["route"]

    try:
        # Получаем локации для выбранного маршрута
        locations = route_locations[city][route]
        city_var = globals().get(city.upper().replace(" ", "_"), city)

        # Формируем сообщение с локациями
        locations_text = "\n".join([f"{loc}" for loc in locations])
        bot.send_message(
            message.chat.id,
            f"🏙 *{city_var} — {route}*\n\n{locations_text}",
            parse_mode="Markdown"
        )

    except KeyError:
        support_markup = types.InlineKeyboardMarkup()
        helpb = types.InlineKeyboardButton(text = "Поддержка", url = support_chell)
        startb = types.InlineKeyboardButton(text ="Занова", callback_data = "send_start")
        support_markup.row(helpb, startb)
        bot.send_message(
            message.chat.id,
            HELPIK,
            reply_markup=support_markup
        )

    current_state.update({
        "step1": False,
        "step2": False,
        "step3": False,
        "step4": False,
        "step5": True
    })

# Данные о городах
cities = [
    {"n": "Москва", "a": True, "s": False},
    {"n": "Белгород", "a": True, "s": False},
    {"n": "Старый Оскол", "a": True, "s": False},
    {"n": "Губкин", "a": True, "s": False}
]

bot.infinity_polling()