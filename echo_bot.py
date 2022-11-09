import traceback

from config_bot import *
import telebot
import logging

from util_function import *

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.

bot = telebot.TeleBot(TEST_TOKEN, parse_mode='Markdown')


def extract_arg(arg):
    return arg.split()[1:]


@bot.message_handler(commands=['proposalsFromId'])
def handle_proposals_from_id(message):
    chat_id = message.chat.id
    args = extract_arg(message.text)
    start_id = int(args[0])
    output, df = get_proposals_from_id(start_id)
    data = open(output, 'rb')
    bot.send_document(chat_id, data)
    os.remove(output)


@bot.message_handler(commands=['approvalsFromDay'])
def handle_approvals_from_day(message):
    chat_id = message.chat.id
    args = extract_arg(message.text)
    start_date = args[0]
    output, df = get_proposals_approvals_from_day(start_date)
    data = open(output, 'rb')
    bot.send_document(chat_id, data)
    os.remove(output)


@bot.message_handler(commands=['help'])
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
