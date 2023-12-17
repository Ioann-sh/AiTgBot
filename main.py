import telebot

from settings import SETTINGS
from manager.AI.AI import AI
from manager.DB.DB import DB

bot = telebot.TeleBot(SETTINGS['TG']['TOKEN'], parse_mode=None)
ai = AI(SETTINGS['AI'])

#COMMANDS
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
                     "For any questions please contact @Ioann_business")

@bot.message_handler(commands=['reg'])
def reg(message):
    bot.send_message('5508618680',
                     f'{message.from_user.id} {message.from_user.first_name} {message.from_user.username}\nWANTS TO REGISTER')

#MAIN
@bot.message_handler(content_types=['text'], func=lambda message: True)
def handle_text(message):
    db = DB(SETTINGS['DB'])

    if (message.reply_to_message is not None) and \
            (str(message.from_user.id) == "5508618680") and \
            (message.text.split()[0] == "reg"):
        print(message.reply_to_message.text)
        user_id = message.reply_to_message.text.split()[0]
        name = message.reply_to_message.text.split()[1]
        db.registration(name, user_id)
        bot.send_message(user_id,
                         "Are you registered!\nEnjoy your use!")
    else:
        if (db.getUserByUserId(message.from_user.id)):
            print(db.getUserByUserId(message.from_user.id))
            #bot.send_message(message.chat.id, ai.chat(message.text))
            bot.send_message(message.chat.id, "хуй")
        else:
            bot.send_message(message.chat.id,
                             "Your profile was not found\n"
                             "Enter the /reg command and wait for you to be registered")

bot.infinity_polling()