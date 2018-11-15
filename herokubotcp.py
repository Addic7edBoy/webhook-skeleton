import telebot
import os
from flask import Flask, request
import logging
import config
import time
from telebot import types


def generate_markup(x):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    if x == 1:
        list_items = [1, 2, 3, 4, 5]
        for item in list_items:
            markup.add(item)
    if x == 0:
        list_items = ['Da', 'No']
        for item in list_items:
            markup.add(item)
    if x == 2:
        list_items = ['Еще', 'Хватит ']
        for item in list_items:
            markup.add(item)
    return markup

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
    else:
        bot.send_message(message.chat.id, 'Основной функционал недоступен, отстань тварь')
        bot.send_message(message.chat.id, 'Но могу скинуть музыку, хочешь?')
        markup = generate_markup(0)
        keyboard_hider = types.ReplyKeyboardRemove()
        if message.text == 'Da':
            bot.send_message(message.chat.id, 'sosi tvar', reply_markup=markup)
        if message.text == 'No':
            bot.send_message(message.chat.id, 's', reply_markup=markup)


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
