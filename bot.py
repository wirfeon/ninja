#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import json
import os
from copy import copy
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Chat
from datetime import datetime

PORT = int(os.environ.get('PORT', '8443'))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# Group title : Group id
# Bot forwards messages from group identified by title to group identified by id
pairing = {
    "Simulator": -1001265460962
}

def admin(bot, update):
    logger.info(update.message.chat.id)
    if (update.message.chat.title not in pairing):
        return

    chat_id = pairing[update.message.chat.title]

    if (update.message.chat.username):
        bot.send_message(chat_id, "Alert in https://t.me/%s/%s" % (update.message.chat.username, update.message.message_id))
    else:
        bot.send_message(chat_id, "Alert in %s" % update.message.chat.title)

def check(bot, update):
    logger.info("'%s'" % updatae.message.text.strip())
    if (update.message.text.strip() in ("/admin", "/ban", "/kick", "/spam", "/scam")):
        admin(bot, update)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)
    update.message.chat.send_message("Error")

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(os.environ["BOT_TOKEN"], workers = 1)

    i = 0
    while i < 2:
        try:
            updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=os.environ["BOT_TOKEN"])
            updater.bot.set_webhook(os.environ["WEB_HOOK"] + os.environ["BOT_TOKEN"])
            break
        except Exception as e:
            logger.warn("Exception: %s" % e)
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

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
