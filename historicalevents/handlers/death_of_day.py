from datetime import datetime

import requests

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger
from historicalevents.utils.get_historical import *
from historicalevents.utils.month import *


def get_deaths_of_the_day(CHANNEL):
    try:
        today = datetime.now()
        day = today.day
        month = today.month

        response = requests.get(
            f'https://en.wikipedia.org/api/rest_v1/feed/onthisday/deaths/{month}/{day}',
            headers={
                'accept': 'application/json; charset=utf-8; profile="https://www.mediawiki.org/wiki/Specs/onthisday/0.3.3"'
            },
        )

        if response.status_code == 200:
            data = response.json()
            deaths = data.get('deaths', [])

            if len(deaths) > 0:
                death_messages = []

                for index, death in enumerate(deaths[:5], start=1):
                    name = f"<b>{death.get('text', '')}</b>"
                    info = death.get('pages', [{}])[0].get(
                        'extract', 'Information not available.'
                    )
                    date = death.get('year', 'Date unknown.')

                    death_message = f'<i>{index}.</i> <b>Name:</b> {name}\n<b>Information:</b> {info}\n<b>Date of death:</b> {date}'
                    death_messages.append(death_message)

                message = f'<b>⚰️ | Deaths on this day: {day} of {get_month_name(month)}</b>\n\n'
                message += '\n\n'.join(death_messages)
                message += '\n\n💬 Did you know? Follow @today_in_historys.'

                bot.send_message(CHANNEL, message)
            else:
                logger.info('-' * 50)
                logger.info(
                    'No information available for deceased individuals for the current day.'
                )
                logger.info('-' * 50)
        else:
            logger.info('-' * 50)
            logger.warning('Error fetching information:', response.status_code)
            logger.info('-' * 50)

    except Exception as e:
        logger.info('-' * 50)
        logger.error('Error sending deaths to the channel:', str(e))
        logger.info('-' * 50)


def hist_channel_death():
    try:
        get_deaths_of_the_day(CHANNEL)
        logger.success(f'Deaths sent to the channel {CHANNEL}')
    except Exception as e:
        logger.info('Error sending death job:', str(e))
