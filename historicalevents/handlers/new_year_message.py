from datetime import datetime

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger
from historicalevents.utils.get_historical import *
from historicalevents.utils.month import *

def new_year_message():
    try:
        photo_url = 'https://i.imgur.com/mlRcKgU.jpeg'

        caption = f'The Today in History channel wishes you a Happy New Year! 🎉🎆✨\n\nMay the upcoming year be filled with joy, success, and new achievements. Let\'s continue learning more and continue the journey for knowledge!\n\nAnd let\'s explore more about history together!'

        bot.send_photo(CHANNEL, photo_url, caption=caption)

    except Exception as e:
        logger.error('Error sending New Year message:', str(e))
