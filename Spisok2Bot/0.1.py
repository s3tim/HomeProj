import telebot
from telebot import types

bot = telebot.TeleBot("7970047574:AAEL7j4lsTYbRzE4dYa7YEm2LYSzZh2o-Pg")  # Замените на реальный токен

@bot.callback_query_handler(func=lambda call: call.data == "edit_text")
def edit_text(call):
    bot.edit_message_text("Текст изменен! ✅", chat_id=call.message.chat.id, message_id=call.message.message_id)
    

@bot.message_handler(commands=["start"])
def send_clickable_text(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Нажми меня", callback_data="edit_text"))
    
    bot.send_message(message.chat.id,"f", reply_markup=markup)
    
bot.infinity_polling()