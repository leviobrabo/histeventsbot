import json
from datetime import datetime

from telebot import types

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger
from historicalevents.utils.get_historical import *


def send_historical_events_channel(CHANNEL):
    try:
        today = datetime.now()
        day = today.day
        month = today.month
        events = get_historical_events()

        if events:
            message = f'<b>TODAY IN HISTORY</b>\n\n📅 | Event on <b>{day}/{month}</b>\n\n{events}\n\n<blockquote>💬 Did you know? Follow @today_in_historys and access our website histday.com.</blockquote>'
            bot.send_message(CHANNEL, message)
        else:
            bot.send_message(
                CHANNEL,
                '<b>No historical events for today.</b>',
                parse_mode='HTML',
            )

            logger.info(
                f'No historical event for today in the group {CHANNEL}'
            )

    except Exception as e:

        logger.error('Error sending historical facts to the channel:', str(e))


def hist_channel():
    try:
        send_historical_events_channel(CHANNEL)

        logger.success(f'Historical events sent to channel {CHANNEL}')

    except Exception as e:

        logger.error(
            'Error in the task of sending historical facts to the channel:',
            str(e),
        )
