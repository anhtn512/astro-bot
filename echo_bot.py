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
    output, df = get_approvals_from_day(start_date)
    data = open(output, 'rb')
    bot.send_document(chat_id, data)
    os.remove(output)


@bot.message_handler(commands=['proposalsFromDay'])
def handle_approvals_from_day(message):
    chat_id = message.chat.id
    args = extract_arg(message.text)
    start_date = args[0]
    output, df = get_proposals_from_day(start_date)
    data = open(output, 'rb')
    bot.send_document(chat_id, data)
    os.remove(output)


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.reply_to(message, """
	🤖 *Nearweek agent bot*
	
	⚙️ Command:
	/proposalsFromId {start ID} : get all proposals from start ID to the latest
	/proposalsFromDay {start day}: get all proposals from start day to current (format of day MMDDYYYY)
	/approvalsFromDay {start day}: get all proposals which has approved from start day to current (format of day MMDDYYYY)
	
	Ex:
	/proposalsFromId 1860  ==> (1860 => latest)
	/proposalsFromDay 11012022 ==> (11/01/2022 => present)
	/approvalsFromDay 11012022 ==> (11/01/2022 => present)
	
	------------------------------
	_If you have any good ideas that you would like me to implement
	Don't be shy, feel free to tell me (@anhtn512)_
	""")


while True:
    print("start")
    try:
        bot.polling()
    except Exception as e:
        print(traceback.format_exc(e))
