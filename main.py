import telebot

from datetime import datetime, timedelta

from settings import SETTINGS
from manager.AI.AI import AI
from manager.DB.DB import DB

bot = telebot.TeleBot(SETTINGS['TG']['TOKEN'], parse_mode=None)
ai = AI(SETTINGS['AI'])

adminId = SETTINGS['ADMIN']['ID']
adminName = SETTINGS['ADMIN']['USERNAME']

context_cache = {}  # словарь с контекстом

CONTEXT_CACHE_INTERVAL = timedelta(minutes=10)


@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.language_code == "ru":
        bot.send_message(message.chat.id,
                         "Здравствуйте, я чат-бот Иоанна на базе ChatGPT версии 3.5-turbo. Задавайте свои вопросы.")
    else:
        bot.send_message(message.chat.id,
                         "Hello, I'm an Ioann's bot based on ChatGPT version 3.5-turbo. Ask your questions.")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     f'For any questions please contact {adminName}')


@bot.message_handler(commands=['reg'])
def reg(message):
    bot.send_message(adminId,
                     f'{message.from_user.id} {message.from_user.first_name} {message.from_user.username}\nWANTS TO REGISTER')


# MAIN
@bot.message_handler(content_types=['text'], func=lambda message: True)
def handle_text(message):
    db = DB(SETTINGS['DB'])
    # регистрация пользователя
    if (message.reply_to_message is not None) and \
            (str(message.from_user.id) == adminId) and \
            (message.text.split()[0] == "reg"):
        print(message.reply_to_message.text)
        user_id = message.reply_to_message.text.split()[0]
        name = message.reply_to_message.text.split()[1]
        db.registration(name, user_id)
        bot.send_message(user_id,
                         "Are you registered!\nEnjoy your use!")

    # обработчик ответа
    else:
        if db.getUserByUserId(message.from_user.id):

            # контекс в кэше
            if message.chat.id in context_cache and datetime.now() - \
                    context_cache[message.chat.id]['timestamp'] <= CONTEXT_CACHE_INTERVAL:
                context = context_cache[message.chat.id]['message']
            # контекст в бд
            else:
                context = db.getContext(message.from_user.id)

            try:
                print(db.getUserByUserId(message.from_user.id))
                # bot.send_message(message.chat.id, message.text)
                bot.send_message(message.chat.id, ai.chat(message.text, context))
                db.addContext(str(message.chat.id), context + message.text, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))    # сохрание контекста в БД
                context_cache[message.chat.id] = {'message': context + message.text, 'timestamp': datetime.now()}   # сохрание контекста в кэше
            except Exception as e:
                bot.send_message(message.chat.id, f"An error occurred while processing your request")
                print(e)
        # если пользователя нет в БД
        else:
            bot.send_message(message.chat.id,
                             "Your profile was not found\n"
                             "Enter the /reg command and wait for you to be registered")


bot.infinity_polling()
