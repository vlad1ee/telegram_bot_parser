import telebot
from telebot import types
import akipress

bot = telebot.TeleBot('1232708633:AAHMuNIog5qrE34jrT4pPmRyJG6sZPPBCHk')
# news_title, single_news = akipress.main()
news_title = None
single_news = None
choice = 0

@bot.message_handler(commands = ['start'])
def hello(message):
    global news_title, single_news
    news_title, single_news = akipress.main()
    btn = types.ReplyKeyboardMarkup(True, True)
    btn.row('Показать меню')
    bot.send_message(message.chat.id, 'Приветствую тебя', reply_markup=btn)

@bot.message_handler(content_types = ['text'])
def say_bye(message):
    my_list = ['пока', 'bye']
    if message.text.lower() in my_list:
        bot.send_message(message.chat.id, text ='До свидания')
    if message.text.lower() == 'показать меню':
        button1 = types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
        button1.row('News title')
        bot.send_message(message.chat.id, text = 'Below you can see the \'News title\' button', reply_markup = button1)
        bot.register_next_step_handler(message, click_button1)


def click_button1(message):
    chat_id = message.chat.id
    if message.text == 'News title':
        bot.send_message(message.chat.id, f'{news_title}\nВЫБЕРИТЕ НОМЕР НОВОСТИ')
        bot.register_next_step_handler(message, get_news)

def get_news(message):
    global choice
    l1 = []
    for i in range(21):
        l1.append(str(i))
    if message.text in l1:
        markup = types.ReplyKeyboardMarkup(True, True)
        button3 = types.KeyboardButton('Photo')
        button4 = types.KeyboardButton('Description')
        markup.add(button3, button4)
        choice = int(message.text)
        bot.send_message(message.chat.id, text='Выберите фото или описание', reply_markup=markup)
        bot.register_next_step_handler(message, get_data)
    else:
        bot.send_message(message.chat.id, f'{news_title}\nТАКОЙ НОВОСТИ НЕ СУЩЕСТВУЕТ\nВЫБЕРИТЕ НОМЕР НОВОСТИ')
        bot.register_next_step_handler(message, get_news)

def get_data(message):
    global choice
    info = single_news[choice]
    if message.text == 'Photo':
        try:
            markup = types.ReplyKeyboardMarkup(True, True)
            button3 = types.KeyboardButton('Description')
            button4 = types.KeyboardButton('Back')
            markup.add(button3, button4)
            bot.send_photo(message.chat.id, info['Photo'], reply_markup= markup)
            bot.register_next_step_handler(message, go_back)
        except:
            bot.send_message(message.chat.id, f'{news_title}\nФОТО ОТСУТСТВУЕТ\nВЫБЕРИТЕ НОВОСТЬ ПО НОМЕРУ')
            bot.register_next_step_handler(message, get_news)
    elif message.text =='Description':
        try:
            markup = types.ReplyKeyboardMarkup(True, True)
            button5 = types.KeyboardButton('Photo')
            button6 = types.KeyboardButton('Back')
            markup.add(button5, button6)
            bot.send_message(message.chat.id, info['Description'], reply_markup=markup)
            bot.register_next_step_handler(message, go_back)
        except:
            bot.send_message(message.chat.id, f'{news_title}\nОПИСАНИЕ ОТСУТСТВУЕТ\nВЫБЕРИТЕ НОВОСТЬ ПО НОМЕРУ')
            bot.register_next_step_handler(message, get_news)

def go_back(message):
    if message.text == 'Back':
        bot.send_message(message.chat.id, f'{news_title}\nВЫБЕРИТЕ НОВОСТЬ ПО НОМЕРУ')
        bot.register_next_step_handler(message, get_news)
    elif message.text == 'Photo':
        try:
            btns = types.ReplyKeyboardMarkup(True, True)
            btn1 = types.KeyboardButton('Quit')
            btn2 = types.KeyboardButton('To menu')
            btns.add(btn1, btn2)
            bot.send_photo(message.chat.id, info['Photo'], reply_markup=btns)
            bot.register_next_step_handler(message, do_finally)
        except:
            bot.send_message(message.chat.id, f'{news_title}\nФОТО ОТСУТСТВУЕТ\nВЫБЕРИТЕ НОВОСТЬ ПО НОМЕРУ')
            bot.register_next_step_handler(message, get_news)
    elif message.text == 'Description':
        try:
            btns2 = types.ReplyKeyboardMarkup(True, True)
            btn3 = types.KeyboardButton('Quit')
            btn4 = types.KeyboardButton('To menu')
            btns2.add(btn3, btn4)
            bot.send_message(message.chat.id, info['Description'], reply_markup=btns2)
            bot.register_next_step_handler(message, do_finally)
        except:
            bot.send_message(message.chat.id, f'{news_title}\nОПИСАНИЕ ОТСУТСТВУЕТ\nВЫБЕРИТЕ НОВОСТЬ ПО НОМЕРУ')
            bot.register_next_step_handler(message, get_news)

def do_finally(message):
    if message.text == 'To menu':
        bot.send_message(message.chat.id, f'{news_title}\nВЫБЕРИТЕ НОВОСТЬ ПО НОМЕРУ')
        bot.register_next_step_handler(message, get_news)
    elif message.text == 'Quit':
        bot.register_next_step_handler(message, hello)

   
bot.polling()