from telebot import types


# Кнопка отправки номера
def num_button():
    # Создание пространства
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создание кнопок
    but1 = types.KeyboardButton('Отправить номер📞',
                                request_contact=True)
    # Добавление кнопок в пространство
    kb.add(but1)

    return kb


# Кнопки главного меню
def main_menu(products):
    # Создание пространства
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создаем сами кнопки
    cart = types.InlineKeyboardButton(text='Корзина🛒', callback_data='cart')
    all_products = [types.InlineKeyboardButton(text=i[1], callback_data=i[0])
                    for i in products]
    # Добавление кнопок в пространство
    kb.add(*all_products)
    kb.row(cart)

    return kb


# Кнопки выбора количества
def choose_count_buttons(pr_amount, plus_or_minus='', amount=1):
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=3)
    # Создаем сами кнопки
    minus = types.InlineKeyboardButton(text='-', callback_data='decrement')
    plus = types.InlineKeyboardButton(text='+', callback_data='increment')
    count = types.InlineKeyboardButton(text=str(amount), callback_data=str(amount))
    to_cart = types.InlineKeyboardButton(text='В корзину🛒', callback_data='to_cart')
    back = types.InlineKeyboardButton(text='Назад🔙', callback_data='back')

    # Алгоритм изменения кол-ва
    if plus_or_minus == 'increment':
        if amount < pr_amount:
            count = types.InlineKeyboardButton(text=str(amount+1), callback_data=str(amount))
    elif plus_or_minus == 'decrement':
        if amount > 1:
            count = types.InlineKeyboardButton(text=str(amount-1), callback_data=str(amount))

    # Добавляем кнопки в пространство
    kb.add(minus, count, plus, back, to_cart)
    return kb

# Кнопки корзины
def cart_buttons():
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создаем сами кнопки
    but1 = types.InlineKeyboardButton(text='Назад🔙', callback_data='back')
    but2 = types.InlineKeyboardButton(text='Оформить заказ🧾', callback_data='order')
    but3 = types.InlineKeyboardButton(text='Очистить корзину🗑️', callback_data='clear')
    # Добавляем кнопки в пространство
    kb.add(but1, but3)
    kb.row(but2)
    return kb


# Кнопка отправки локации
def loc_button():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем кнопку
    but1 = types.KeyboardButton('Отправить геопозицию📍', request_location=True)
    # Добавляем кнопки в пространство
    kb.add(but1)
    return kb
