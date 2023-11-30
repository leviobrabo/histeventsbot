import json
from datetime import datetime

from telebot import types

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger
from historicalevents.utils.get_historical import *


def send_historical_events_user(user_id):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        user = search_user(user_id)
        events = get_historical_events()

        markup = types.InlineKeyboardMarkup()
        channel_ofc = types.InlineKeyboardButton(
            'Official Channel 🇧🇷', url='https://t.me/today_in_historys'
        )
        markup.add(channel_ofc)

        if events:
            message = f'<b>TODAY IN HISTORY</b>\n\n📅 | Event on <b>{day}/{month}</b>\n\n{events}'
            sent_message = bot.send_message(
                user_id, message, parse_mode='HTML', reply_markup=markup
            )
            message_id = sent_message.message_id

            set_user_message_id(user_id, message_id)
        else:
            bot.send_message(
                user_id,
                '<b>No historical events for today.</b>',
                parse_mode='HTML',
                reply_markup=markup,
            )
            logger.info('-' * 50)
            logger.warning(
                f'No historical event for today for user {user_id}'
            )
            logger.info('-' * 50)

    except Exception as e:
        logger.info('-' * 50)
        logger.error(
            'Error sending historical facts to users:', str(e)
        )
        logger.info('-' * 50)


def hist_user_job():
    try:
        user_models = get_all_users({'msg_private': 'true'})
        for user_model in user_models:
            user_id = user_model['user_id']
            message_id = user_model['message_id']

            if message_id:
                try:
                    bot.delete_message(user_id, message_id)
                except Exception as e:
                    logger.info('-' * 50)
                    logger.warning(f'Could not delete {user_id}')
                    logger.info('-' * 50)
                    pass

            send_historical_events_user(user_id)
            logger.info('-' * 50)
            logger.success(f'Message sent to user {user_id}')
            logger.info('-' * 50)
    except Exception as e:
        logger.info('-' * 50)
        logger.error('Error sending to users:', str(e))
        logger.info('-' * 50)
