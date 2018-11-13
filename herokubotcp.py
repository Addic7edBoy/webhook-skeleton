import logging
import os
import telebot
import cherrypy
import config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher

bot = telebot.TeleBot(config.token)


class WebhookServer(object):
    @cherrypy.expose
    def __init__(self, TOKEN, NAME):
        super(WebhookServer, self).__init__()
        self.TOKEN = TOKEN
        self.NAME = NAME
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)

if __name__ == "__main__":
    # Set these variable to the appropriate values
    TOKEN = "640239383:AAF2VMnsgzpEqzKd7tYCoRC3MvNYxZJf4wA"
    NAME = "webhook-test-gb"
    PORT = os.environ.get('PORT')

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    cherrypy.config.update({'server.socket_host': '0.0.0.0', })
    cherrypy.config.update({'server.socket_port': int(PORT), })
    cherrypy.tree.mount(WebhookServer(TOKEN, NAME),
                        "/{}".format(TOKEN),
                        {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})
    cherrypy.engine.start()