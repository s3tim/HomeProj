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
    "Для того чтобы создать план напишите:\nПлан\n1. задача\n2. задача"
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

FILE_PATH = "NFUW.xlsx" 
if Path(FILE_PATH).exists():
    df = pd.read_excel(FILE_PATH, engine="openpyxl")
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

import re

def format_text(text):
    # Сохраняем оригинальный текст для даты
    original_text = text
    
    # Убираем лишние пробелы
    text = ' '.join(text.split())
    
    # Ищем дату в тексте
    date_pattern = r'\d{1,2}\.\d{1,2}\.(?:\d{2}|\d{4})'
    date_match = re.search(date_pattern, text)
    date_str = date_match.group() if date_match else ""
    
    # Удаляем дату из текста для обработки задач
    if date_str:
        text = re.sub(re.escape(date_str), '', text)
    
    # Ищем задачи в разных форматах
    pattern1 = r'(?<!\S)(\d+)[\.\)\*/][\s*]*([^\n]*?)(?=\s*(?:\d+[\.\)\*/][\s*]*|~|$))'
    pattern2 = r'~\s*([^\n~]*?)(?=\s*~|$)'
    
    # Парсим задачи первого формата (нумерованные)
    tasks1 = re.findall(pattern1, text)
    numbered_tasks = [(num, task.strip()) for num, task in tasks1 if task.strip()]
    
    # Парсим задачи второго формата (с тильдой)
    tasks2 = re.findall(pattern2, text)
    special_tasks = [task.strip() for task in tasks2 if task.strip()]
    
    # Форматируем результат
    if date_str:
        result = f"План на {date_str}:\n"
    else:
        result = date_str

    # Обрабатываем нумерованные задачи
    if numbered_tasks:
        # Исправляем нумерацию (на случай ошибок пользователя)
        corrected_tasks = []
        expected_number = 1
        
        for original_num, task in numbered_tasks:
            try:
                current_num = int(original_num)
                # Если номер не по порядку, исправляем его
                if current_num != expected_number:
                    corrected_tasks.append((expected_number, task))
                else:
                    corrected_tasks.append((current_num, task))
                expected_number += 1
            except ValueError:
                # Если номер не число, используем ожидаемый номер
                corrected_tasks.append((expected_number, task))
                expected_number += 1
        
        for number, task in corrected_tasks:
            result += f"{number}) {task}\n"
    
    # Обрабатываем задачи с тильдой (нумеруем с 1)
    elif special_tasks:
        for i, task in enumerate(special_tasks, 1):
            result += f"{i}) {task}\n"
    
    # Если задачи не найдены, возвращаем оригинальный текст с очисткой
    else:
        result = original_text.strip()
    
    return result

#На план            доделай новые проверки на то что есть ли текст и вот это все
@bot.message_handler(func=lambda message: (NFUC[0] in ["Button", "Text"]) and (any(keyword.lower() in message.text.lower() for keyword in exclude_words)))
def ide_plan1(message):
    user_id = message.from_user.id  #это id челла
    new_entry = {"A": user_id, "B": NFUC[0], "C": NFUC[1]}
    user_entry = next((entry for entry in NFUCs if entry.get("A") == user_id), None)
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
            termo = '|'.join(map(re.escape, exdate))
            mtD = re.sub(termo, '', mtD).strip()
            if not mtD or mtD.isspace():
                bot.send_message(message.chat.id, randomNo)
                bot.send_message(message.chat.id, Hi[10])
            else:
                if any(word in mtD.lower() for word in wor):
                    if not formatted_text or formatted_text.isspace() or not mtD or mtD.isspace():
                        bot.send_message(message.chat.id, randomNo)
                        bot.send_message(message.chat.id, Hi[10])
                    else:
                        NFUC[1] = f"{formatted_text}"
                        bot.send_message(message.chat.id, NFUC[1])
                        #ЭТО ДЛЯ СОХРАНЕНИЯ В ТАБЛИЦУ
                        user_entry = next((entry for entry in NFUCs if entry.get("A") == user_id), None)
                        if not user_entry:
                            NFUCs.append(new_entry)
                            pd.DataFrame(NFUCs).to_excel(FILE_PATH, engine="openpyxl", index=False) 
                        else:
                            plan_columns = [col for col in user_entry.keys() if col not in ['A', 'B'] and str(col).isdigit()]
                            if plan_columns:
                                #Находим максимальный номер столбца с планами
                                max_plan_col = max(int(col) for col in plan_columns)
                                next_plan_col = str(max_plan_col + 1)
                            else:
                                next_plan_col = "2"
                            user_entry[next_plan_col] = f"План на {exdate}:\n{NFUC[3]}"
                            user_entry["B"] = NFUC[0]
                            user_entry["C"] = NFUC[1]
                        pd.DataFrame(NFUCs).to_excel(FILE_PATH, engine="openpyxl", index=False)
                    print(NFUCs)
                else:
                    pattern = '|'.join(map(re.escape, wor))
                    mtD = re.sub(pattern, '', mtD).strip()
                    NFUC[1] = f"План на {exdate}:\n{mtD}"
                    bot.edit_message_text(NFUC[1], chat_id=message.chat.id, message_id=message.message_id)
        else:
            NFUC[3] = formatted_text
            NFUC[1] = current_date
            bot.send_message(message.chat.id, f"План на {NFUC[1]}?", reply_markup=markuP)
        

@bot.callback_query_handler(func=lambda call: call.data.startswith("IDE_P1"))
def call_P1(call):
    if call.data == "IDE_P1_Y":
        NFUC[2] = "callback_PY"
        NFUC[1] = f"План на {NFUC[1]}:\n{NFUC[3]}"
        bot.edit_message_text(NFUC[1], chat_id=call.message.chat.id, message_id=call.message.message_id)
    if call.data == "IDE_P1_N":
        NFUC[2] = "callback_PN"
        bot.send_message(call.message.chat.id, Hi[9])
    button(call.message)

@bot.message_handler(func=lambda message: NFUC[2] == "callback_PN")
def CLN(message):
    user_id = message.from_user.id  #это id челла
    new_entry = {"A": user_id, "B": NFUC[0], "C": NFUC[3]}
    exdate = extract_date(message.text)
    randomNo = random.choice(NoPlane)

    if not message.text or message.text.isspace():
        bot.send_message(message.chat.id, randomNo)
        bot.send_message(message.chat.id, Hi[10])
    else:
        if exdate:
            #ЭТО ДЛЯ СОХРАНЕНИЯ В ТАБЛИЦУ
            user_entry = next((entry for entry in NFUCs if entry.get("A") == user_id), None)
            if not user_entry:
                NFUCs.append(new_entry)
                pd.DataFrame(NFUCs).to_excel(FILE_PATH, engine="openpyxl", index=False) 
            else:
                plan_columns = [col for col in user_entry.keys() if col not in ['A', 'B'] and str(col).isdigit()]
                if plan_columns:
                    #Находим максимальный номер столбца с планами
                    max_plan_col = max(int(col) for col in plan_columns)
                    next_plan_col = str(max_plan_col + 1)
                else:
                    next_plan_col = "2"
                user_entry[next_plan_col] = f"План на {exdate}:\n{NFUC[3]}"
                user_entry["B"] = NFUC[0]
                user_entry["C"] = NFUC[1]
                pd.DataFrame(NFUCs).to_excel(FILE_PATH, engine="openpyxl", index=False)
                NFUC[3] = user_entry[next_plan_col]
                bot.send_message(message.chat.id, NFUC[3])
            print(NFUCs)

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
