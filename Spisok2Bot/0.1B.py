import telebot
from telebot import TeleBot, types
import time
from openpyxl import Workbook, load_workbook
import time
import threading
from queue import Queue
import pandas as pd
from pathlib import Path
import re
from datetime import datetime

bot = telebot.TeleBot("7970047574:AAEL7j4lsTYbRzE4dYa7YEm2LYSzZh2o-Pg")

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
    "На какую дату план?",
    "Напишите дату выполнения задачи"
]

NFUC = ["NFUC","NFUC","NFUC"]

NFUCs = [
    {"A": "NAME", "B": "SETINGS"}
]

FILE_PATH = "NFU.ods"
if Path(FILE_PATH).exists():
    df = pd.read_excel(FILE_PATH, engine="odf")
    NFUCs = df.to_dict("records")  # Конвертируем DataFrame в список словарей
else:
    print("Ошибка с таблицами")

def extract_date(text):
    """Извлекает первую найденную дату в формате DD.MM.YY или DD.MM.YYYY, анализируя только первые 3 слова"""
    words = text.split()[:3]  # Получаем первые 3 слова
    for word in words:
        # Проверяем точное соответствие формату даты
        if re.fullmatch(r'\d{1,2}\.\d{1,2}\.(?:\d{2}|\d{4})', word):
            return word
    return None

exclude_words = ["план", "plane", "/plane"]
def format_text(text):
    # 1. Добавляем точки после цифр (если их нет)
    text = re.sub(r'(\d+)([^\d.])', r'\1.\2', text)
    
    # 2. Разделяем задачи через Enter
    text = text.replace(';', '\n')  # Заменяем точки с запятой на переносы
    text = re.sub(r'(\d+\.)\s*', r'\n\1 ', text)  # Перенос перед цифрами с точкой
    return text.strip()

#На план
@bot.message_handler(func=lambda message: (NFUC[0] in ["Button", "Text"]) and (any(keyword.lower() in message.text.lower() for keyword in ["план", "plane", "/plane"])))
def ide_plan1(message):
    user_id = message.from_user.id  #это id челла
    new_entry = {"A": user_id, "B": NFUC[0], "C": NFUC[1]}
    current_date = datetime.now().strftime("%d.%m.%Y")

    markuP = types.InlineKeyboardMarkup()
    markuP.row(
        types.InlineKeyboardButton("Да", callback_data="IDE_P1_Y"),
        types.InlineKeyboardButton("Нет", callback_data="IDE_P1_N")
    )

    mtD = " ".join([word for word in message.text.split() 
                   if word.lower() not in [w.lower() for w in exclude_words]])
    exdate = extract_date(message.text)
    if exdate is not None:
        mtD = mtD.replace(exdate, '').strip()
        if mtD in ["на"]:
            NFUC[1] = f"План на {exdate}\n{mtD}"
        else:
            mtD = mtD.replace("на", "").strip()
            NFUC[1] = f"План на {exdate}\n{mtD}" if mtD else f"План на {exdate}"
        bot.send_message(message.chat.id, NFUC[1])
    else:
        mt = " ".join([word for word in message.text.split() if word not in exclude_words])
        formatted_text = format_text(mt)
        NFUC[1] = f"План на {current_date}\n{formatted_text}"
        bot.send_message(message.chat.id, f"План на {current_date}?", reply_markup=markuP)


    # Ищем запись, где в столбце "A" (или другом) есть user_id ЭТО ДЛЯ СОХРАНЕНИЯ В ТАБЛИЦУ
    user_entry = next((entry for entry in NFUCs if entry.get("A") == user_id), None)
    if user_entry:
        user_entry["B"] = NFUC[0]
        user_entry["С"] = NFUC[1]
    else:
        NFUCs.append(new_entry)
    pd.DataFrame(NFUCs).to_excel(FILE_PATH, engine="odf", index=False)
    print(NFUCs)

    #if NFUC[2] == "callback_P1":


@bot.callback_query_handler(func=lambda call: call.data.startswith("IDE_P1") )
def call_P1(call):
    if call.data == "IDE_P1_Y":
        bot.send_message(call.message.chat.id, NFUC[1])
    if call.data == "IDE_P1_N":
        bot.send_message(call.message.chat.id, Hi[9])
        NFUC[2] == "callback_P1"                                                               #Вот от сюда пиши дальше в ide_plan1
    button(call.message)

@bot.message_handler(func=lambda message: NFUC and NFUC[0] == "SETINGS" and any(keyword in message.text for keyword in ["Идея", "идея", "Idea", "idea"]))
def ide_plan2(message):
    bot.send_message(message.chat.id, "SAE2")

@bot.callback_query_handler(func=lambda call: call.data == "edit_text1" )
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
    user_id = message.from_user.id 
    # Ищем запись, где в столбце "A" (или другом) есть user_id
    user_entry = next((entry for entry in NFUCs if entry.get("A") == user_id), None)
    if user_entry:
        NFUC[0] = user_entry["B"]

    SOS[0] = "SOS"  # Сбрасываем состояние
    user_id = message.from_user.id  #это id челла

    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(Hi[1], callback_data="edit_text1"),
        types.InlineKeyboardButton(Hi[2], callback_data="edit_text2")
    )
    bot.send_message(message.chat.id, Hi[0], reply_markup=markup)

#Здесь код для режима кнопок
@bot.message_handler(func=lambda message: SOS[0] == "edit_text1")
def button(message):
    NFUC[0] = "Button"
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

@bot.message_handler(func=lambda message: NFUC and NFUC[0] == "Button")
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
    NFUC[0] = "Text"
    SOS[0] = "SOS"

bot.infinity_polling()
