import telebot
import os
from flask import Flask, request
import logging
import config
import time
bot = telebot.TeleBot(config.token)

# Здесь пишем наши хэндлеры


@bot.message_handler(func=lambda message: True, content_types=["text"])
def gb_strong(message):
    if message.text == 'Хэй бот скинь свой любимый трек':
        f = open('photo2.jpg', 'rb')
        v = open('music/GB_squad.ogg', 'rb')
        bot.send_photo(message.chat.id, f)
        bot.send_voice(message.chat.id, v)
    if message.text == 'Ты ебанутый?':
        time.sleep(0.2)
        bot.send_message(message.chat.id, 'Закройся лох это шедевр')
    if message.text == 'Я создал монстра':
        time.sleep(0.3)
        bot.send_message(message.chat.id, 'Я тебя щас забаню кожаный ублюдок')


#@bot.message_handler(func=lambda message: True, content_types=['text'])
#def echo_message(message):
#    bot.reply_to(message, message.text)

if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)

    @server.route("/", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200

    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://webhook-test-gb.herokuapp.com/")
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    bot.remove_webhook()
    bot.polling(none_stop=True)
