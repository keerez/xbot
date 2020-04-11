#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import sys
import random
import re
import logging
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
 

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    """Send a message when the command /start is issued."""
    usr_name = (update.message.from_user.first_name) + '! =)'
    greeting = 'Hi, '
    hint = ''' To find out what I can type : /help '''
    bot_reply_message = (greeting + usr_name + hint)
    update.message.reply_text(bot_reply_message)



def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('''Help!
    You can request these functions from the "lang_helper" :
    /random for recive randome wrong sentence, which needs to be fixed
    /word <WORD> for get the meaning of the <WORD>''')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


global initial_sentances
initial_sentances = (list(open('/home/xbot/python/sentence')))

def random_line(update, context):
    s_print = random.choice(list(initial_sentances))
    words = s_print.split() 
    random.shuffle(words)
    words_ready = (" ".join(str(x) for x in words))
    words_complited = re.sub('[?!@#$,."]','', words_ready)
    update.message.reply_text(words_complited)

def check_message_from_user(update, context):
    corrected_sentence = update.message.text
    #corrected_sentence = re.sub('/check', '', update.message.text)
    open_file = open('/home/xbot/python/sentence')
    print(open_file)
    for line in open_file:
        if corrected_sentence in line:
            update.message.reply_text('Yes')
            break
        else:
            update.message.reply_text('No')
            break



def word_description(update, context):
    app_id = "9187736f"
    app_key = "92b7569c22c8f386f99eac69c300f083"
    language = "en-gb"
    word_id = update.message.text.split()
    url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word_id[1].lower()
    r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    result = r.json()
    try:
        word_mean = (result["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0])
        update.message.reply_text(json.dumps(word_mean))
    except:
        update.message.reply_text('The meaning of your word not found! =(')

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1227395367:AAHg13VCjaag8F85xQP0hHr7JQT7NI2yu1Y", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("random", random_line))
    dp.add_handler(CommandHandler("word", word_description))
    dp.add_handler(CommandHandler("check", check_message_from_user))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

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
