import telebot
from telebot import TeleBot, types
import time
from openpyxl import load_workbook

bot = telebot.TeleBot("7970047574:AAEL7j4lsTYbRzE4dYa7YEm2LYSzZh2o-Pg")
wb = load_workbook('BackUp.xlsx')

#Для состояния и нуммерации задач
SOS = ["SOS", "TaskState"]  # Изначально в главном меню

#Для всех слов бота
Hi = [
    "Привет! Я умный помощник...\nВыбери режим",
    "Кнопки",
    "Текст",
    "Режим выбран ✅",
    "Хорошо, теперь выбери количество\nЕсли твоих задачь больше, просто напиши их количество в чат",
    "Теперь отправь свои задачи",
    "верно?",
    "Напишите новое число",
]

@bot.callback_query_handler(func=lambda call: call.data == "edit_text1")
def callback_buttons(call):
    SOS[0] = "edit_text1"  # Изменяем первый элемент списка
    bot.edit_message_text(Hi[3], chat_id=call.message.chat.id, message_id=call.message.message_id)
    button(call.message)  # Переходим в режим кнопок

@bot.callback_query_handler(func=lambda call: call.data == "edit_text2")
def callback_text(call):
    SOS[0] = "edit_text2"  # Изменяем первый элемент списка
    bot.edit_message_text(Hi[3], chat_id=call.message.chat.id, message_id=call.message.message_id)
    text(call.message)  # Переходим в текстовый режим

@bot.message_handler(commands=["start"])
def start(message):
    SOS[0] = "SOS"  # Сбрасываем состояние
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(Hi[1], callback_data="edit_text1"),
        types.InlineKeyboardButton(Hi[2], callback_data="edit_text2")
    )
    bot.send_message(message.chat.id, Hi[0], reply_markup=markup)

#Здесь код для режима кнопок
@bot.message_handler(func=lambda message: SOS[0] == "edit_text1")
def button(message):
    markup1 = types.InlineKeyboardMarkup()
    markup1.row(
        types.InlineKeyboardButton("1", callback_data="task1"),
        types.InlineKeyboardButton("2", callback_data="task2"),
        types.InlineKeyboardButton("3", callback_data="task3"),
        types.InlineKeyboardButton("4", callback_data="task4"),
        types.InlineKeyboardButton("5", callback_data="task5")
    )
    if SOS[0] == "edit_text1":
        SOS[0] = "SOS"
        bot.send_message(message.chat.id, Hi[4], reply_markup=markup1)
        return

@bot.message_handler()
def button2(message):
    if SOS[0] == "SOS" and message.text.isdigit():
        task_num = message.text
        markup2 = types.InlineKeyboardMarkup()
        markup2.row(
            types.InlineKeyboardButton("Да", callback_data=f"task{task_num}"),
            types.InlineKeyboardButton("Нет", callback_data="t_button")
        )
        SOS[0] = f"task{task_num}"
        SOS[1] = f"{task_num}"
        bot.send_message(message.chat.id, text=f"{message.text} {Hi[6]}", reply_markup=markup2)
    
    for i in range(1, 10000):
        if SOS[1] == f"{i}" and SOS[0] == "t_but":
            SOS[0] = "call"
            SOS[1] = f"{i}"
            break

    for i in range(1, 10000):
        if SOS[1] in [f"{i}"] and SOS[0] == "call":
            SOS[0] = "SOS"
            SOS[1] = f"{i}"
            bot.send_message(message.chat.id, SOS[1])
            break
            
@bot.callback_query_handler(func=lambda call: call.data.startswith("task"))
def callback_task(call):
    SOS[0] = "task"
    SOS[1] = f"{call.data}"
    bot.edit_message_text(Hi[3], chat_id=call.message.chat.id, message_id=call.message.message_id)
    for i in range(1, 10000):
        if call.data == f"task{i}": #call.data это как message.text
            SOS[0] = "call"
            SOS[1] = f"{i}"
            break

    button2(call.message)      #СУПЕР НАДО ставь эту тему вроде для перехода

@bot.callback_query_handler(func=lambda call: call.data.startswith("t_button")) #ЭТО ПИШИ НА НЕТ
def callback_task(call):
    SOS[0] = "t_but"
    bot.edit_message_text(Hi[7], chat_id=call.message.chat.id, message_id=call.message.message_id)
    button2(call.message)

#Здесь код для текстового режима
@bot.message_handler(func=lambda message: SOS[0] == "edit_text2")
def text(message):
    bot.send_message(message.chat.id, "text2")

bot.infinity_polling()

#ДОБАВЬ УДАЛЕНИЕ 
#И ТАБЛИЦЫ