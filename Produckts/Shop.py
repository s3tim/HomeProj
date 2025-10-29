import telebot
from telebot import types

# Инициализация бота (замени "bot" на реальный токен)
bot = telebot.TeleBot("7970047574:AAEL7j4lsTYbRzE4dYa7YEm2LYSzZh2o-Pg", parse_mode=None)

# Временное хранилище данных (замени на БД в продакшене)
users = {}  # users[chat_id] = {'role': 'user/admin', 'cart': [], ...}
products = {
    1: {'name': 'Товар 1', 'price': 100, 'description': 'Описание 1', 'available': True},
    2: {'name': 'Товар 2', 'price': 200, 'description': 'Описание 2', 'available': True}
}
orders = {}
admins = []  # ID админов (добавляются через /addadmin)

# ==================== ОСНОВНЫЕ КОМАНДЫ ====================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    if chat_id not in users:
        users[chat_id] = {'role': 'user', 'cart': []}
    
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn_products = types.KeyboardButton('🛍️ Товары')
    btn_cart = types.KeyboardButton('🛒 Корзина')
    btn_orders = types.KeyboardButton('📦 Мои заказы')
    if is_admin(chat_id):
        btn_admin = types.KeyboardButton('👨‍💼 Админ-панель')
        markup.add(btn_products, btn_cart, btn_orders, btn_admin)
    else:
        markup.add(btn_products, btn_cart, btn_orders)
    
    bot.send_message(chat_id, "Добро пожаловать в магазин!", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '🛍️ Товары')
def show_products(message):
    chat_id = message.chat.id
    for prod_id, product in products.items():
        if product['available']:
            markup = types.InlineKeyboardMarkup()
            btn_add = types.InlineKeyboardButton(
                "➕ Добавить в корзину", 
                callback_data=f"add_{prod_id}"
            )
            markup.add(btn_add)
            caption = f"{product['name']}\nЦена: {product['price']} руб.\n{product['description']}"
            bot.send_photo(chat_id, photo=open('product_image.jpg', 'rb'), caption=caption, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '🛒 Корзина')
def show_cart(message):
    chat_id = message.chat.id
    cart = users[chat_id]['cart']
    if not cart:
        bot.send_message(chat_id, "Корзина пуста")
        return
    total = 0
    text = "🛒 Ваша корзина:\n"
    for item in cart:
        product = products[item['product_id']]
        text += f"{product['name']} - {item['quantity']} шт. = {product['price'] * item['quantity']} руб.\n"
        total += product['price'] * item['quantity']
    text += f"Общая сумма: {total} руб."
    markup = types.InlineKeyboardMarkup()
    btn_clear = types.InlineKeyboardButton("🧹 Очистить корзину", callback_data="clear_cart")
    btn_order = types.InlineKeyboardButton("✅ Оформить заказ", callback_data="create_order")
    markup.add(btn_clear, btn_order)
    bot.send_message(chat_id, text, reply_markup=markup)

# ==================== АДМИН-ПАНЕЛЬ ====================
def is_admin(chat_id):
    return chat_id in admins

@bot.message_handler(func=lambda message: message.text == '👨‍💼 Админ-панель' and is_admin(message.chat.id))
def admin_panel(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn_add = types.KeyboardButton('➕ Добавить товар')
    btn_edit = types.KeyboardButton('✏️ Редактировать товар')
    btn_orders = types.KeyboardButton('📦 Заказы')
    btn_back = types.KeyboardButton('⬅️ Назад')
    markup.add(btn_add, btn_edit, btn_orders, btn_back)
    bot.send_message(chat_id, "Админ-панель:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '➕ Добавить товар' and is_admin(message.chat.id))
def add_product(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Введите данные товара в формате: Название|Цена|Описание")
    bot.register_next_step_handler(msg, process_product_data)

def process_product_data(message):
    chat_id = message.chat.id
    try:
        name, price, description = message.text.split('|')
        new_id = max(products.keys()) + 1
        products[new_id] = {
            'name': name,
            'price': int(price),
            'description': description,
            'available': True
        }
        bot.send_message(chat_id, "Товар добавлен!")
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка: {e}")

# ==================== CALLBACK-ОБРАБОТЧИКИ ====================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    if call.data.startswith("add_"):
        prod_id = int(call.data.split("_")[1])
        users[chat_id]['cart'].append({'product_id': prod_id, 'quantity': 1})
        bot.answer_callback_query(call.id, "Товар добавлен в корзину!")
    elif call.data == "clear_cart":
        users[chat_id]['cart'] = []
        bot.answer_callback_query(call.id, "Корзина очищена")
        bot.delete_message(chat_id, call.message.message_id)
    elif call.data == "create_order":
        # Логика оформления заказа
        order_id = len(orders) + 1
        orders[order_id] = {
            'user_id': chat_id,
            'items': users[chat_id]['cart'].copy(),
            'status': 'новый'
        }
        users[chat_id]['cart'] = []
        bot.answer_callback_query(call.id, "Заказ оформлен!")
        bot.send_message(chat_id, f"Ваш заказ №{order_id} принят в обработку")
        # Уведомление админов
        for admin_id in admins:
            bot.send_message(admin_id, f"Новый заказ №{order_id}")

# ==================== ЗАПУСК ====================
if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()