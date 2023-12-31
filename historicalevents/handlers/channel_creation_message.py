import time
from datetime import datetime

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger
from historicalevents.utils.get_historical import *
from historicalevents.utils.month import *

# Channel creation date
data_criacao = datetime(2022, 11, 19)


def send_anniversary_message(CHANNEL):
    try:
        current_date = datetime.now()

        if (
            current_date.month == data_criacao.month
            and current_date.day == data_criacao.day
        ):
            years_created = current_date.year - data_criacao.year

            if years_created == 1:
                message = f'Today, the Today in History channel is celebrating its 1st anniversary! 🎉🎂🎈'
            else:
                message = f'Today, the Today in History channel is celebrating its {years_created} years of existence! 🎉🎂🎈'

            bot.send_message(CHANNEL, message)

    except Exception as e:
        logger.error('Error sending anniversary message:', str(e))


def schedule_anniversary():
    while True:
        now = datetime.now()
        next_anniversary = datetime(
            now.year, data_criacao.month, data_criacao.day, 0, 0, 0
        )

        if now >= next_anniversary:
            next_anniversary = datetime(
                now.year + 1, data_criacao.month, data_criacao.day, 0, 0, 0
            )

        wait_time = (next_anniversary - now).total_seconds()
        time.sleep(wait_time)

        send_anniversary_message(CHANNEL)
