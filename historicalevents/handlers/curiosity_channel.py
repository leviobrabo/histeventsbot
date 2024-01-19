import json
from datetime import datetime

import pytz

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger
from historicalevents.utils.get_historical import *
from historicalevents.utils.month import *


def get_curiosity(CHANNEL):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        with open(
            './historicalevents/data/curisity.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)
            curiosity = json_events.get(f'{month}-{day}', {}).get(
                'curiosity', []
            )
            if curiosity:
                info = curiosity[0].get('text', '')

                # For 2025 (uncomment this line and comment the line above)
                # info = curiosidade[1].get("texto1", "")

                message = f'<b>Historical Curiosities 📜</b>\n\n{info}\n\n<blockquote>💬 Did you know? Follow @today_in_historys.</blockquote>'
                bot.send_message(CHANNEL, message)
            else:

                logger.info('No information available for today.')

    except Exception as e:

        logger.error('Error fetching information:', str(e))


def hist_channel_curiosity():
    try:
        get_curiosity(CHANNEL)

        logger.success(f'Curiosity sent to the channel {CHANNEL}')

    except Exception as e:

        logger.error('Error sending curiosity job:', str(e))
