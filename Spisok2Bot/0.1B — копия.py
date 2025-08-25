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
import random

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
    "Напишите дату выполнения задачи",
    "Для того чтобы создать план напишите\nПлан:\n1. задача\n2. задача"
]

NoPlane = [
    "Если твой план — ничего не делать, то у тебя идеальный шанс провести день идеально",
    "Когда твой план — просто быть, весь день становится идеальным отпуском от суеты",
    "План ничего — единственная стратегия, где перевыполнение гарантировано",
    "Если твоя цель — ничего, то каждый шаг — это уже достижение",
    "Хочешь быть продуктивным? Выполни план ничего — и ты уже молодец",
    "Никаких тревог, дедлайнов и стресса. План ничего — лучший антистресс-менеджмент",
    "План ничего — потому что иногда самая сложная работа — это отдыхать",
    "Когда твой план — ничего, ты открываешь пространство для всего",
    "Не делать — тоже действие. Не планировать — тоже план",
    "План ничего — это искусство быть, а не казаться",
    "Самый надежный план? Ничего не ждать — и тогда всё будет приятным бонусом"
]

NFUC = ["NFUC","NFUC","NFUC","NFUC"]

NFUCs = [
    {"A": "NAME", "B": "SETINGS"}
]

FILE_PATH = "NFU.ods"
if Path(FILE_PATH).exists():
    df = pd.read_excel(FILE_PATH, engine="odf")
    NFUCs = df.to_dict("records")  # Конвертируем DataFrame в список словарей
else:
    print("Ошибка с таблицами")

def get_random_message():
    return random.choice(messages_list)

def extract_date(text):
    """Извлекает первую найденную дату в формате DD.MM.YY или DD.MM.YYYY, анализируя только первые 3 слова"""
    words = text.split()[:3]  # Получаем первые 3 слова
    for word in words:
        # Проверяем точное соответствие формату даты
        if re.fullmatch(r'\d{1,2}\.\d{1,2}\.(?:\d{2}|\d{4})', word):
            return word
    return None

exclude_words = ["план", "plane", "/plane", "plane in", "plane for", "план на"]
wor = ["на", "for", "in"]

def format_text(text):
    # 1. Добавляем точки после цифр (если их нет)
    text = re.sub(r'(\d+)([^\d.])', r'\1.\2', text)
    
    # 2. Разделяем задачи через Enter
    text = text.replace(';', '\n')  # Заменяем точки с запятой на переносы
    text = re.sub(r'(\d+\.)\s*', r'\n\1 ', text)  # Перенос перед цифрами с точкой
    return text.strip()

#На план            доделай новые проверки на то что есть ли текст и вот это все
@bot.message_handler(func=lambda message: (NFUC[0] in ["Button", "Text"]) or (any(keyword.lower() in message.text.lower() for keyword in exclude_words)))
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

    formatted_text = format_text(mtD)
    exdate = extract_date(message.text)
    randomNo = random.choice(NoPlane)

    if not formatted_text or formatted_text.isspace():
        bot.send_message(message.chat.id, randomNo)
        bot.send_message(message.chat.id, Hi[10])
    else:
        if exdate is not None:
            mtD = mtD.replace(exdate, "").strip()
            if mtD in wor:
                words = formatted_text.split()
                filtered_words = [word for word in words if word.lower() not in wor and word.lower() not in exdate]
                filtered_text = ' '.join(filtered_words)
                if not filtered_text or filtered_text.isspace():
                    bot.send_message(message.chat.id, randomNo)
                    bot.send_message(message.chat.id, Hi[10])
                else:
                    NFUC[1] = f"План на {exdate}\n{filtered_text}"
                    bot.send_message(message.chat.id, NFUC[1])
            else:
                mtD = mtD.replace(wor, "").strip()
                NFUC[1] = f"План на {exdate}\n{mtD}"
                bot.send_message(message.chat.id, NFUC[1])
        else:
            mts = " ".join([word for word in message.text.split() if word not in exclude_words])
            formatted_text2 = format_text(mts)
            NFUC[3] = formatted_text2
            NFUC[1] = current_date
            bot.send_message(message.chat.id, f"План на {current_date}?", reply_markup=markuP)
        
    # ЭТО ДЛЯ СОХРАНЕНИЯ В ТАБЛИЦУ
    user_entry = next((entry for entry in NFUCs if entry.get("A") == user_id), None)
    if user_entry:
        user_entry["B"] = NFUC[0]
        user_entry["С"] = NFUC[1]
    else:
        NFUCs.append(new_entry)
    pd.DataFrame(NFUCs).to_excel(FILE_PATH, engine="odf", index=False)
    print(NFUCs)

@bot.callback_query_handler(func=lambda call: call.data.startswith("IDE_P1") )
def call_P1(call):
    if call.data == "IDE_P1_Y":
        NFUC[2] = "callback_PY"
        bot.send_message(call.message.chat.id, f"План на {NFUC[1]}\n{NFUC[3]}")
    if call.data == "IDE_P1_N":
        NFUC[2] = "callback_PN"
        bot.send_message(call.message.chat.id, Hi[9])
    button(call.message)

@bot.message_handler(func=lambda message: NFUC[2] == "callback_PN")
def CLN(message):
    user_id = message.from_user.id  #это id челла
    new_entry = {"A": user_id, "B": NFUC[0], "C": NFUC[1]}
    exdate = extract_date(message.text)
    randomNo = random.choice(NoPlane)

    if not message.text or message.text.isspace():
        bot.send_message(message.chat.id, randomNo)
    else:
        user_entry = next((entry for entry in NFUCs if entry.get("A") == user_id), None)
        if user_entry:
            user_entry["B"] = NFUC[0]
            user_entry["С"] = NFUC[1]
        else:
            NFUCs.append(new_entry)
            pd.DataFrame(NFUCs).to_excel(FILE_PATH, engine="odf", index=False)
            print(NFUCs)
            bot.send_message(message.chat.id, f"План на {exdate}\n{NFUC[3]}")



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
