from telebot import types

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger


@bot.message_handler(commands=['help'])
def cmd_help(message):
    try:
        if message.chat.type != 'private':
            return
        user_id = message.from_user.id
        user = search_user(user_id)

        text = "Hello! I'm a bot programmed to send historical facts every day at preset times, starting at 8 AM. \n\nAdditionally, I have some incredible commands that might be useful for you. Feel free to interact with me and discover more about the world around us! \n\n<b>Simply click on one of them:</b>"

        markup = types.InlineKeyboardMarkup()
        commands = types.InlineKeyboardButton(
            'List of commands', callback_data='commands'
        )
        support = types.InlineKeyboardButton(
            'Support', url='https://t.me/updatehist'
        )
        donation = types.InlineKeyboardButton(
            '💰 Donations', url='https://t.me/updatehist'
        )

        markup.add(commands)
        markup.add(support, donation)

        photo = 'https://i.imgur.com/8BCiwvz.png'
        bot.send_photo(
            message.chat.id,
            photo=photo,
            caption=text,
            reply_markup=markup,
        )
    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Error while sending the help message: {e}')
        logger.info('-' * 50)
