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
    message_1 = 'Хэй бот скинь свой любимый трек'
    message_2 = 'Ты ебанутый?'
    message_3 = 'Я создал монстра'
    if not message_1 or message_2 or message_3:
        bot.send_message(message_1.chat.id, 'Основной функционал недоступен, отстань тварь')
        markup = generate_markup(0)
        bot.send_message(message_1.chat.id, 'Но могу скинуть музыку, хочешь?', reply_markup=markup)
        keyboard_hider = types.ReplyKeyboardRemove()
        if message.text == 'Da':
            markup = generate_markup(1)
            bot.send_message(message.chat.id, 'Выбирай', reply_markup=markup)
        if message.text == 'No':
            bot.send_message(message.chat.id, 'sosi', reply_markup=keyboard_hider)
    else:
        if message.text == message_1:
            f = open('photo2.jpg', 'rb')
            v = open('music/GB_squad.ogg', 'rb')
            bot.send_photo(message.chat.id, f)
            bot.send_voice(message.chat.id, v)
        if message.text == message_2:
            time.sleep(0.2)
            bot.send_message(message.chat.id, 'Закройся лох это шедевр')
        if message.text == message_3:
            time.sleep(0.3)
            bot.send_message(message.chat.id, 'Я тебя щас забаню кожаный ублюдок')

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
