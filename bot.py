#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
import json
import os
from copy import copy
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime

PORT = int(os.environ.get('PORT', '8443'))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

pairing = {
    "Test": ""
}

def admin(bot, update):
    logger.info(update.message.chat.id)
    #bot.send_message(pairing[update.chat.title], "Alert")

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)
    update.message.chat.send_message("Coming soon...")

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(os.environ["BOT_TOKEN"], workers = 1)

    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=os.environ["BOT_TOKEN"])
    updater.bot.set_webhook(os.environ["WEB_HOOK"] + os.environ["BOT_TOKEN"])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("admin", admin))

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
