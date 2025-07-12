import telebot
import buttons
import database


# Создаем объект бота
bot = telebot.TeleBot('TOKEN')
# Создаем временные данные
users = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # Проверяем юзера на наличие в БД
    if database.check_user(user_id):
        bot.send_message(user_id, 'Добро пожаловать!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите пункт меню:',
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))
    else:
        bot.send_message(user_id, 'Здравствуйте! Давайте начнем регистрацию!'
                                  'Напишите свое имя',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        # Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)


# Этап получения имени
def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, 'Отлично! Теперь отправьте свой номер!',
                     reply_markup=buttons.num_button())
    # Переход на этап получения номера
    bot.register_next_step_handler(message, get_num, user_name)


# Этап получения номера
def get_num(message, user_name):
    user_id = message.from_user.id
    # Проверка на правильность номера
    if message.contact:
        user_num = message.contact.phone_number
        database.register(user_id, user_name, user_num)
        bot.send_message(user_id, 'Регистрация прошла успешно!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Отправьте номер по кнопке!')
        # Возвращаем на этап получения номера
        bot.register_next_step_handler(message, get_num, user_name)


# Выбор кол-ва товара
@bot.callback_query_handler(lambda call: call.data in ['increment', 'decrement', 'to_cart', 'back'])
def choose_count(call):
    user_id = call.message.chat.id

    if call.data == 'increment':
        bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                      reply_markup=buttons.choose_count_buttons(
                                          database.get_exact_pr(users[user_id]['pr_name'])[3], 'increment',
                                      users[user_id]['pr_count']))
        users[user_id]['pr_count'] += 1
    elif call.data == 'decrement':
        bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                      reply_markup=buttons.choose_count_buttons(
                                          database.get_exact_pr(users[user_id]['pr_name'])[3], 'decrement',
                                          users[user_id]['pr_count']))
        users[user_id]['pr_count'] -= 1
    elif call.data == 'to_cart':
        pr_name = database.get_exact_pr(users[user_id]['pr_name'])[1]
        database.add_to_cart(user_id, pr_name, users[user_id]['pr_count'])
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, 'Товар успешно помещен в корзину!',
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))
    elif call.data == 'back':
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, 'Выберите пункт меню:',
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))


# Обработчик команды /admin
@bot.message_handler(commands=['admin'])
def admin(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Чтобы добавить товар, впишите все в следующем порядке:\n'
                              'Название, описание, количество, цена, ссылка на фото\n\n'
                              'Фотографии загружать на https://postimages.org/. Отправляйте прямую ссылку на фото!',
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    # Переход на этап получения товара
    bot.register_next_step_handler(message, get_pr)


# Этап получения товара
def get_pr(message):
    user_id = message.from_user.id
    pr_info = message.text.split(',')
    database.add_pr_to_db(pr_info[0].strip(), pr_info[1].strip(), int(pr_info[2]), float(pr_info[3]), pr_info[4].strip())
    bot.send_message(user_id, 'Продукт успешно добавлен!')


@bot.callback_query_handler(lambda call: int(call.data) in [i[0] for i in database.get_all_pr()])
def choose_product(call):
    user_id = call.message.chat.id
    pr_info = database.get_exact_pr(int(call.data))
    bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
    bot.send_photo(user_id, photo=pr_info[-1], caption=f'{pr_info[1]}\n\n'
                                                       f'Описание: {pr_info[2]}\n'
                                                       f'Цена: {pr_info[4]}\n'
                                                       f'Количество на складе: {pr_info[3]}',
                   reply_markup=buttons.choose_count_buttons(pr_info[3]))
    users[user_id] = {'pr_name': int(call.data), 'pr_count': 1}


# Запуск бота
bot.polling(non_stop=True)
