import json
from datetime import datetime

from telebot import types

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger
from historicalevents.utils.get_historical import *


def send_historical_events_group(chat_id):
    try:
        today = datetime.now()
        day = today.day
        month = today.month

        chat = search_group(chat_id)
        topic = chat.get('thread_id')
        events = get_historical_events()

        markup = types.InlineKeyboardMarkup()
        channel_ofc = types.InlineKeyboardButton(
            'Official Channel 🇧🇷', url='https://t.me/today_in_historys'
        )
        markup.add(channel_ofc)

        if events:
            message = f'<b>TODAY IN HISTORY</b>\n\n📅 | Event on <b>{day}/{month}</b>\n\n{events}'
            bot.send_message(
                chat_id,
                message,
                parse_mode='HTML',
                reply_markup=markup,
                message_thread_id=topic,
            )

            logger.success(
                f'Successfully sent historical events to group {chat_id}'
            )

        else:
            bot.send_message(
                chat_id,
                '<b>No historical events for today.</b>',
                parse_mode='HTML',
                reply_markup=markup,
                message_thread_id=topic,
            )

            logger.warning(f'No historical event for today in group {chat_id}')

    except Exception as e:

        logger.error('Error sending historical facts to chats:', str(e))

        remove_chat_db(chat_id)

        logger.warning(
            f'Chat {chat_id} removed from the database due to an error while sending historical events message.'
        )


def hist_chat_job():
    try:
        chat_models = get_all_chats()
        for chat_model in chat_models:
            chat_id = chat_model['chat_id']
            if chat_id != GROUP_LOG:
                try:
                    send_historical_events_group(chat_id)
                except Exception as e:

                    logger.error(
                        f'Error sending historical events to group {chat_id}: {str(e)}'
                    )

    except Exception as e:

        logger.error('Error while sending to chats:', str(e))
