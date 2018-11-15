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
        list_items = ['1', '2', '3', '4', '5']
        for item in list_items:
            markup.add(item)
    if x == 0:
        list_items = ['Da', 'No']
        for item in list_items:
            markup.add(item)
    if x == 2:
        list_items = ['Еще', 'Ненада']
        for item in list_items:
            markup.add(item)
    return markup

bot = telebot.TeleBot(config.token)


@bot.message_handler(func=lambda message: message.text == 'Хэй бот скинь свой любимый трек')
def command_hey(message):
    f = open('photo2.jpg', 'rb')
    v = open('music/GB_squad.ogg', 'rb')
    bot.send_photo(message.chat.id, f)
    bot.send_voice(message.chat.id, v)


@bot.message_handler(func=lambda message: message.text == 'Ты ебанутый?')
def command_e(message):
    time.sleep(0.2)
    bot.send_message(message.chat.id, 'Закройся лох это шедевр')


@bot.message_handler(func=lambda message: message.text == 'Я создал монстра')
def command_m(message):
    time.sleep(0.3)
    bot.send_message(message.chat.id, 'Я тебя щас забаню кожаный ублюдок')


@bot.message_handler(func=lambda message: True, content_types=["text"])
def gb_strong(message):
    bot.send_message(message.chat.id, 'Основной функционал недоступен, отстань тварь')
    markup = generate_markup(0)
    msg = bot.send_message(message.chat.id, 'Но могу скинуть музыку, хочешь?', reply_markup=markup)
    bot.register_next_step_handler(msg, first_step)


def first_step(message):
    keyboard_hider = types.ReplyKeyboardRemove()
    if message.text == 'Da':
        markup = generate_markup(1)
        msg = bot.send_message(message.chat.id, 'Выбирай', reply_markup=markup)
        bot.register_next_step_handler(msg, second_step)
    if message.text == 'No':
        bot.send_message(message.chat.id, 'sosi', reply_markup=keyboard_hider)


def second_step(message):
    markup = generate_markup(0)
    if message.text == '1':
        v = open('music/balthazar.ogg', 'rb')
        bot.send_voice(message.chat.id, v, None,  reply_markup=markup)
        msg = bot.send_message(message.chat.id, 'Еще?', reply_markup=markup)
    elif message.text == '2':
        v = open('music/eden.ogg', 'rb')
        bot.send_voice(message.chat.id, v, None, reply_markup=markup)
        msg = bot.send_message(message.chat.id, 'Еще?', reply_markup=markup)
    elif message.text == '3':
        v = open('music/grandson.ogg', 'rb')
        bot.send_voice(message.chat.id, v, None, reply_markup=markup)
        msg = bot.send_message(message.chat.id, 'Еще?', reply_markup=markup)
    elif message.text == '4':
        v = open('music/grandson.ogg', 'rb')
        bot.send_voice(message.chat.id, v, None, reply_markup=markup)
        msg = bot.send_message(message.chat.id, 'Еще?', reply_markup=markup)
    elif message.text == '5':
        v = open('music/oxxxy.ogg', 'rb')
        bot.send_voice(message.chat.id, v, None)
        msg = bot.send_message(message.chat.id, 'Еще?', reply_markup=markup)
    bot.register_next_step_handler(msg, first_step)


def third_step(message):
    keyboard_hider = types.ReplyKeyboardRemove()
    if message.text == 'Ненада':
        bot.send_message(message.chat.id, 'sosi', reply_markup=keyboard_hider)
    if message.text == 'Еще':
        bot.send_message(message.chat.id, 'sosi', reply_markup=keyboard_hider)
        message = 'Da'
        bot.register_next_step_handler(message, first_step)


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
