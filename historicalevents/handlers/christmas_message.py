from datetime import datetime

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger
from historicalevents.utils.get_historical import *
from historicalevents.utils.month import *


def christmas_message():
    try:
        photo_url = 'https://i.imgur.com/YRnwSxX.png'

        caption = f"The Today in History channel wishes you a Merry Christmas! 🎊❤️🎉\n\nChristmas is more than a celebration, it's a new chance for us to reinvent ourselves and become better people. A Merry and beautiful Christmas to everyone!\n\nAnd let's learn more information about history!"

        bot.send_photo(CHANNEL, photo_url, caption=caption)

    except Exception as e:
        logger.error('Error sending Christmas message:', str(e))
