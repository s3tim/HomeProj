import telebot
from telebot import TeleBot, types
import time

bot = telebot.TeleBot("7970047574:AAEL7j4lsTYbRzE4dYa7YEm2LYSzZh2o-Pg")

#Для состояния
SOS = ["SOS"]  # Изначально в главном меню

#Для нуммерации задач
TaskState = ["TaskState"]
user_data = {} 

#Для всех слов бота
Hi = [
    "Привет! Я умный помощник...\nВыбери режим",
    "Кнопки",
    "Текст",
    "Режим выбран ✅",
    "Хорошо, теперь выбери количество\nЕсли твоих задачь больше, просто напиши их количество в чат",
    "Теперь отправь свои задачи",
    "верно?",
    "Напишите новое число"
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
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("1", callback_data="task1"),
        types.InlineKeyboardButton("2", callback_data="task2"),
        types.InlineKeyboardButton("3", callback_data="task3"),
        types.InlineKeyboardButton("4", callback_data="task4"),
        types.InlineKeyboardButton("5", callback_data="task5")
    )

    if message.text.isdigit():  #если что-то из этого есть в сообщении оно проходит дальше
        SOS[0] = f"task{message.text}"
        TaskState[0] = f"{message.text}"
        markup2 = types.InlineKeyboardMarkup()
        markup2.row(
            types.InlineKeyboardButton("Да", callback_data=f"task{message.text}"),
            types.InlineKeyboardButton("Нет", callback_data="task_button")
        )
        bot.send_message(message.chat.id, text=f"{message.text} {Hi[6]}", reply_markup=markup2)
    
    if SOS[0] == "edit_text1":
        bot.send_message(message.chat.id, Hi[4], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("task"))
def callback_task(call):
    #bot.send_message(call.message.chat.id, "WW")
    #if call.data == "task_button":
    #    bot.send_message(call.message.chat.id, Hi[7])
    #    #TaskState[0] == f"{call.message.text}"
    #    SOS[0] = f"task{call.message.text}"

    #if call.data == "task1":
    #    SOS[0] = f"task1"
    #    markup3 = types.InlineKeyboardMarkup()
    #    markup3.row(
    #        types.InlineKeyboardButton("Да", callback_data=f"task1"),
    #        types.InlineKeyboardButton("Нет", callback_data="task_button")
    #    )
    #    bot.send_message(message.chat.id, Hi[5], reply_markup=markup3)
    user_data[message.chat.id] = message.text
    

def test(message):
    saved_text = user_data.get(call.message.chat.id, "❌ Данные не найдены")
    bot.send_message(call.message.chat.id, f"Ваш текст: {saved_text}")

#Здесь код для текстового режима
@bot.message_handler(func=lambda message: SOS[0] == "edit_text2")
def text(message):
    bot.send_message(message.chat.id, "text2")

bot.infinity_polling()