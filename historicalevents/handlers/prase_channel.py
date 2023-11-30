import json
from datetime import datetime

import pytz

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger
from historicalevents.utils.get_historical import *
from historicalevents.utils.month import *


def get_quote(CHANNEL):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        with open(
            './historicalevents/data/prase.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            quote_info = json_events.get(f'{month}-{day}')
            if quote_info:
                quote = quote_info.get('quote', '')
                author = quote_info.get('author', '')

                message = f'<b>💡 Quote for reflection</b>\n\n"<i>{quote}"</i> - <b>{author}</b>\n\n💬 Did you know? Follow @today_in_historys.'
                bot.send_message(CHANNEL, message)
            else:
                logger.info('-' * 50)
                logger.info('There is no information for today.')
                logger.info('-' * 50)
    except Exception as e:
        logger.info('-' * 50)
        logger.error('Error retrieving information:', str(e))
        logger.info('-' * 50)


def hist_channel_quote():
    try:
        get_quote(CHANNEL)
        logger.info('-' * 50)
        logger.success(f'Quote sent to channel {CHANNEL}')
        logger.info('-' * 50)
    except Exception as e:
        logger.info('-' * 50)
        logger.error('Error sending quote:', str(e))
        logger.info('-' * 50)
