#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import json
import os
import time
import sys
from copy import copy
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Chat
from datetime import datetime

_port = int(os.environ.get('PORT', '9000'))
_webhook = "%s%s" % (os.environ["WEB_HOOK"], os.environ["BOT_TOKEN"])
_token = os.environ["BOT_TOKEN"]
_location = os.environ["URL_LOCATION"]
_certificate = os.environ["CERTIFICATE"]
_listen = "127.0.0.1"

# Enable logging
logging.basicConfig(stream=sys.stderr, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)

# Group title : Group id
# Bot forwards messages from group identified by title to group identified by id
pairing = {
    "Simulator": -1001265460962,
    "NEM::Red": -1001265460962,
    "NEM Czech & Slovak Republic": -1001265460962,
    "NEMberia 2.0": -1001265460962
}

def admin(bot, update):
    logger.info("Title: '%s' ID: %d" % (update.message.chat.title, update.message.chat.id))
    if (update.message.chat.title not in pairing):
        return

    chat_id = pairing[update.message.chat.title]

    if (update.message.chat.username):
        bot.send_message(chat_id, "Alert in https://t.me/%s/%s" % (update.message.chat.username, update.message.message_id))
    else:
        bot.send_message(chat_id, "Alert in %s" % update.message.chat.title)

def check(bot, update):
    if (update.message.text.strip() in ("/admin", "/ban", "/kick", "/spam", "/scam")):
        admin(bot, update)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, error)

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    logger.info("Creating updater object with token: '%s'" % (_token))

    updater = Updater(_token)

    i = 0
    while i < 2:
        try:
            logger.info("Starting webhook '%s' %d '%s'" % (_listen, _port, _location))
            updater.start_webhook(listen=_listen, port=_port, url_path=_location)
            updater.bot.set_webhook(url=_webhook, certificate=open(_certificate, 'rb'))
            break
        except Exception as e:
            logger.error("Exception: %s" % e)
            updater.stop()
        #endtry

        i += 1
        time.sleep(1)
    #endwhile
 
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("admin", admin))
    dp.add_handler(CommandHandler("ban", admin))
    dp.add_handler(CommandHandler("kick", admin))
    dp.add_handler(CommandHandler("spam", admin))
    dp.add_handler(CommandHandler("scam", admin))
    dp.add_handler(MessageHandler(Filters.text, check))

    # log all errors
    dp.add_error_handler(error)

    logger.info("Running")

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
