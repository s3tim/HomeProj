import telebot
from telebot import types

bot = telebot.TeleBot("8121047623:AAFcWKPqug7rGdyMTN8qOMHa0IenZnvpi0M")

@bot.message_handler(commands=["start"])           #На команду
def main(message):
        bot.send_message(message.chat.id, "Привет")

@bot.message_handler(content_types=['photo'])      #При отправки фото
def get_photo(message):
        markup = types.InlineKeyboardMarkup()          #клавиатура = типо добавитт директорию с кнопками
        btn = types.InlineKeyboardButton("Перейти на сайт", url=("https://chat.deepseek.com/"))
        btn2 = types.InlineKeyboardButton("удалить", callback_data = "delete")
        btn3 = types.InlineKeyboardButton("Отредактировать", callback_data = "edit")
        markup.row(btn)                                #Добавить кнопку c дизайном
        markup.row(btn2, btn3)                               #Добавить кнопку2 и 3 с дизайном
        
        file = open("./image/pass.png", "rb")          #открыть файл на чтение
        bot.send_photo(message.chat.id, file, reply_markup=markup)      #бот скинет фотку

        bot.send_message(                              #Как print для бота
        message.chat.id,                               #объект содеражащий всю инфу о пользователе.подгруппа данных о чате.id пользователя
        "Фото получено! Хочешь перейти на сайт?",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
        if callback.data == "delete":
                bot.delete_message(callback.message.chat.id, callback.message.message_id)
        if callback.data == "edit":
                bot.edit_message_text("текст отредактирован", callback.message.chat.id, callback.message.message_id)


@bot.message_handler(commands=["site", "s"])      #При написание команды 
def site_mes(message):                            #def -- ключевая команда для создания функции    site_mes -- имя фунции      (message) -- параметр куда передается обьект с данными о полученном фото
        markup = types.InlineKeyboardMarkup()          #клавиатура = типо добавить директорию с кнопками
        abtn = types.InlineKeyboardButton("Перейти на сайт", url=("https://chat.deepseek.com/"))
        abtn2 = types.InlineKeyboardButton("удалить", callback_data2="edit")
        markup.add(abtn)                                #Добавить кнопку в ряд
        markup.add(abtn2)                               #Добавить кнопку2 в ряд

        bot.send_message(                              #Как print для бота
        message.chat.id,                               #объект содеражащий всю инфу о пользователе.подгруппа данных о чате.id пользователя
        "Фото получено! Хочешь перейти на сайт?",
        reply_markup=markup
    )






    @bot.message_handler(func=lambda message: message.text.startswith("Маршрут")) #фильтр, срабатывает только если текст начинается с "Маршрут"
def step3(message):#переделать

    if bs == 1:
        if message.text == "Маршрут 1":
            btn = 1
        elif message.text == "Маршрут 2":
            btn = 2
        elif message.text == "Маршрут 3":
            btn = 3
        elif message.text == "Маршрут месяца":
            btn = 4
    
    if btn == 1:
        if message.text == "Маршрут 1":
            bot.send_message(message.chat.id, "Первая локация: спортивный комплекс <b> Хоркина </b>", parse_mode = "html")
    if btn == 2:
        if message.text == "Маршрут 2":
            bot.send_message(message.chat.id, "Первая локация: спортивный комплекс <b> Хоркина </b>", parse_mode = "html")    
    if btn == 3:
        if message.text == "Маршрут 3":
            bot.send_message(message.chat.id, "Первая локация: спортивный комплекс <b> Хоркина </b>", parse_mode = "html")
    if btn == 4:
        if message.text == "Маршрут месяца":
            bot.send_message(message.chat.id, "Первая локация: спортивный комплекс <b> Хоркина </b>", parse_mode = "html")


        if f1[0] is True:
        bs6 = types.KeyboardButton(f1[1])
    if g1[0] is True:
        bs7 = types.KeyboardButton(g1[1])
    if h1[0] is True:
        bs8 = types.KeyboardButton(h1[1])
    if i1[0] is True:
        bs9 = types.KeyboardButton(i1[1])
    if j1[0] is True:
        bs10 = types.KeyboardButton(j1[1])
        markup.row(bs1, bs2)
    markup.row(bs3, bs4, bs5)

bot.infinity_polling()

import telebot
from telebot import types

bot = telebot.TeleBot("7970047574:AAEL7j4lsTYbRzE4dYa7YEm2LYSzZh2o-Pg")

a1 = (True, "Москва")          #активные города true, не активные false
b1 = (True, "Белгород")
c1 = (True, "Старый Оскол")
d1 = (True, "Губкин")
e1 = (False, "ГОРОД")
f1 = (False, "ГОРОД")
g1 = (False, "ГОРОД")
h1 = (False, "ГОРОД")
i1 = (False, "ГОРОД")
j1 = (False, "ГОРОД")



@bot.message_handler(commands=["start"])
def step1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard =True)
    if a1[0] is True:
        bs1 = types.KeyboardButton(a1[1])
    if b1[0] is True:
        bs2 = types.KeyboardButton(b1[1])
    if c1[0] is True:
        bs3 = types.KeyboardButton(c1[1])
    if d1[0] is True:
        bs4 = types.KeyboardButton(d1[1])
    if e1[0] is True:
        bs5 = types.KeyboardButton(e1[1])
    
    markup.row(bs1, bs2)
    markup.row(bs3, bs4)
        

@bot.message_handler(func=lambda message: message.text in ["Москва", "Белгород", "Старый Оскол", "Губкин"])
def step2(message):
    city = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    if city == "Москва": 
        btn1 = types.KeyboardButton("Маршрут 1")
        btn2 = types.KeyboardButton("Маршрут 2")
        btn3 = types.KeyboardButton("Маршрут 3")
        btn4 = types.KeyboardButton("Маршрут месяца")
        markup.row(btn4)
        markup.row(btn1, btn2, btn3)
        bot.send_message(message.chat.id, "Маршруты из города Москва", reply_markup=markup)
    
    elif city == "Белгород": 
        btn1 = types.KeyboardButton("Маршрут 1")
        btn2 = types.KeyboardButton("Маршрут 2")
        btn3 = types.KeyboardButton("Маршрут 3")
        btn4 = types.KeyboardButton("Маршрут 4")
        markup.row(btn1)
        markup.row(btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Маршруты из города Белгород", reply_markup=markup)
    
    elif city == "Старый Оскол": 
        btn1 = types.KeyboardButton("Маршрут 1")
        btn2 = types.KeyboardButton("Маршрут 2")
        btn3 = types.KeyboardButton("Маршрут 3")
        btn4 = types.KeyboardButton("Маршрут 4")
        markup.row(btn1)
        markup.row(btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Маршруты из города Старый Оскол", reply_markup=markup)
    
    elif city == "Губкин": 
        btn1 = types.KeyboardButton("Маршрут 1")
        btn2 = types.KeyboardButton("Маршрут 2")
        btn3 = types.KeyboardButton("Маршрут 3")
        btn4 = types.KeyboardButton("Маршрут 4")
        markup.row(btn1)
        markup.row(btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Маршруты из города Губкин", reply_markup=markup)
        bot.delete_message(callback.message.chat.id, callback.message.message_id -1)
    bot.register_next_step_handler(step3)
    
    msg = bot.send_message(message.chat.id, f"{city}, {route} активирован")
    step3(msg)

reply_markup=types.ReplyKeyboardRemove() #убирает клавиатуру
bot.delete_message(message.chat.id, message.message_id -1)    #доделай удаление всех сообщений после выбора маршрута название маршрута должно остаться
bot.infinity_polling()