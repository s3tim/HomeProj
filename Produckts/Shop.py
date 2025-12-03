# Это шаблон кода для Ресторанного бота
import telebot
import time
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

bot = telebot.TeleBot("7970047574:AAEL7j4lsTYbRzE4dYa7YEm2LYSzZh2o-Pg")

admin = {}
googleT = {
    "en": "f",
    "r": "f"
}

TransN = ""

#Google translator
                                            #Только когда не пустая

def googleTr(text):
    user_text = TransN
    if user_text and user_text.strip:
        # 1. Определяем язык сообщения
        detected_lang = detect(user_text)
        
        # 2. Проверяем, нужен ли перевод (например, если язык не русский)
        if detected_lang != 'ru':
            # Создаем переводчик с автоопределением источника на русский
            translator = GoogleTranslator(source='auto', target='en')
            translated_text = translator.translate(user_text)
            
            # 3. Отправляем результат с информацией об определенном языке
            return( 
                        f"🌐 Определен язык: **{detected_lang}**\n"
                        f"📝 Перевод: **{translated_text}**")
        else:
            # 4. Если сообщение уже на русском
            return(f"✅ Сообщение уже на русском языке. Переводчик не требуется.")

@bot.message_handler(func=lambda message: True)
def a(message):
    global TransN
    TransN = "Человек!"
    print(TransN)
    TransY = googleTr(TransN)
    bot.send_message(TransY)
    #user = bot.user_id
    #if user in admin:
    #    bot.send_message("Привет, админ")
    #    print("Admin activated")
    #    return
    
bot.infinity_polling()