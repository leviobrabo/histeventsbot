from datetime import datetime

import pytz
import requests

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger
from historicalevents.utils.get_historical import *
from historicalevents.utils.month import *


def get_births_of_the_day(CHANNEL):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://en.wikipedia.org/api/rest_v1/feed/onthisday/births/{month}/{day}',
            headers={
                'accept': 'application/json; charset=utf-8; profile="https://www.mediawiki.org/wiki/Specs/onthisday/0.3.3"'
            },
        )

        if response.status_code == 200:
            data = response.json()
            births = data.get('births', [])

            if len(births) > 0:
                birth_messages = []

                for index, birth in enumerate(births[:5], start=1):
                    name = f"<b>{birth.get('text', '')}</b>"
                    info = birth.get('pages', [{}])[0].get(
                        'extract', 'Information not available.'
                    )
                    date = birth.get('year', 'Date unknown.')

                    birth_message = f'<i>{index}.</i> <b>Name:</b> {name}\n<b>Information:</b> {info}\n<b>Date of birth:</b> {date}'
                    birth_messages.append(birth_message)

                message = f'<b>🎂 | Births on this day: {day} {get_month_name(month)}</b>\n\n'
                message += '\n\n'.join(birth_messages)
                message += '\n\n<blockquote>💬 Did you know? Follow @today_in_historys.</blockquote>'

                bot.send_message(CHANNEL, message)
            else:

                logger.info('No information about births today.')

        else:

            logger.warning('Error fetching information:', response.status_code)

    except Exception as e:

        logger.error('Error fetching information:', str(e))


def hist_channel_birth():
    try:
        get_births_of_the_day(CHANNEL)

        logger.success(f'Births sent to the channel {CHANNEL}')

    except Exception as e:

        logger.error('Error sending birth job:', str(e))
