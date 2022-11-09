import os
import traceback

from config_bot import *
import telebot
import logging

from util_function import *
from message_classify import *

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.

bot = telebot.TeleBot(TEST_TOKEN, parse_mode='Markdown')


@bot.message_handler(func=lambda message: check_get_proposals(message.text))
def handle_proposals_from_id(message):
    chat_id = message.chat.id
    text = message.text.split(' ')
    start_id = int(text[1])
    output, df = get_proposals_from_id(start_id)
    data = open(output, 'rb')
    bot.send_document(chat_id, data)
    os.remove(output)


@bot.message_handler(func=lambda message: check_get_approved(message.text))
def handle_approved_from_day(message):
    chat_id = message.chat.id
    text = message.text.split(' ')
    start_date = text[1]
    output, df = get_proposals_approved_from_day(start_date)
    data = open(output, 'rb')
    bot.send_document(chat_id, data)
    os.remove(output)


@bot.message_handler(func=lambda message: check_help_bot(message.text))
def handle_help(message):
    bot.reply_to(message, """
	🤖 *Thanks for your feedback*
	_If you have any good ideas that you would like me to implement
	Don't be shy, feel free to tell me (@anhtn512)_
	""")


while True:
    print("start")
    try:
        bot.polling()
    except Exception as e:
        print(traceback.format_exc(e))
