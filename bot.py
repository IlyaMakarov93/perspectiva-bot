
import config
import telebot
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


name = ''
surname = ''
contacts = ''
age = 0


@bot.message_handler(commands=['start'])
def welcome(message):
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Регистрация")
    item2 = types.KeyboardButton("Сайт РООИ Перспектива")
    item3 = types.KeyboardButton("Контакты")
    item4 = types.KeyboardButton("Наши Мероприятия")

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id,
                     "Добро пожаловать в бот Перспективы.".format(message.from_user, bot.get_me()), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Сайт РООИ Перспектива':
            bot.send_message(message.chat.id,'https://perspektiva-inva.ru/')
        elif message.text == 'Регистрация':
            bot.send_message(message.from_user.id, "Добрый день! Давайте запишем Вас в базу данных! Как Вас зовут?")
            bot.register_next_step_handler(message, reg_name)
        elif message.text == 'Контакты':
            markup = types.InlineKeyboardMarkup()
            btn_vk = types.InlineKeyboardButton(text='Vkontakte', url='https://vk.com/rooiperspektiva')
            btn_fb = types.InlineKeyboardButton(text='Facebook', url='https://www.facebook.com/rooiperspektiva')
            btn_inst = types.InlineKeyboardButton(text = 'Instagram',url='https://www.instagram.com/rooi_perspektiva')
            markup.add(btn_vk,btn_fb,btn_inst)
            bot.send_message(message.chat.id, "Наш номер +7(495)725-39-82. Также Вы можете нам написать в социальные сети", reply_markup=markup)
        elif message.text =="Наши Мероприятия":
            bot.send_message(message.chat.id, 'Все наши актуальные мероприятия по этой ссылке https://perspektiva-inva.ru/news/')




@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text == 'Help':
        bot.reply_to(message, 'Для регистрации в базе данных введите Reg')




def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Какая у Вас фамилия?")
    bot.register_next_step_handler(message, reg_surname)

def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "Запишите Ваши контакты: ")
    bot.register_next_step_handler(message, reg_contacts)

def reg_contacts(message):
    global contacts
    contacts = message.text
    bot.send_message(message.from_user.id, "Сколько вам лет? ")
    bot.register_next_step_handler(message, reg_age)

def reg_age(message):
    global age
    age = message.text

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Вам ' + str(age) + ' лет. Вас зовут: ' + name + ' ' + surname + '. Ваши контакты: '+contacts+'. Все верно?'
    bot.send_message(message.from_user.id, text = question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Хорошо. Вы успешно внесены в базу данных")
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Давайте повторим попытку. ")
        bot.send_message(call.message.chat.id, "Давайте запишем Вас в базу данных! Как Вас зовут?")
        bot.register_next_step_handler(call.message, reg_name)

bot.polling()