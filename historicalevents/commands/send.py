from telebot import types

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger


@bot.message_handler(commands=['sendon'])
def commands_sendon(message):
    try:
        if message.chat.type != 'private':
            return
        user_id = message.from_user.id
        user = search_user(user_id)

        if user:
            if user.get('msg_private') == 'true':
                bot.reply_to(
                    message,
                    'You have ALREADY ACTIVATED the function to receive messages in private chat.',
                )
            else:
                update_msg_private(user_id, 'true')
                bot.reply_to(
                    message,
                    '<b>Private messages ACTIVATED</b>. You will receive historical facts every day at 8 am.',
                )
        else:
            add_user_db(message)
            bot.reply_to(message, 'Send the command again.')

    except Exception as e:
        logger.info('-' * 50)
        print(f'Error activating the receipt of historical events: {str(e)}')
        logger.info('-' * 50)


@bot.message_handler(commands=['sendoff'])
def commands_sendff(message):
    try:
        if message.chat.type != 'private':
            return
        user_id = message.from_user.id
        user = search_user(user_id)

        if user:
            if user.get('msg_private') == 'false':
                bot.reply_to(
                    message,
                    'You have ALREADY DEACTIVATED the function to receive messages in private chat.',
                )
            else:
                update_msg_private(user_id, 'false')
                bot.reply_to(
                    message,
                    '<b>Private messages DEACTIVATED</b>. You will receive historical facts every day at 8 am.',
                )
        else:
            add_user_db(message)
            bot.reply_to(message, 'Send the command again.')

    except Exception as e:
        logger.info('-' * 50)
        print(
            f'Error deactivating the receipt of historical events: {str(e)}'
        )
        logger.info('-' * 50)
