import json
from datetime import datetime

import pytz

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger
from historicalevents.utils.get_historical import *
from historicalevents.utils.month import *


def message_CHANNEL_HISTORY_ALERT():
    try:
        message = "🌟 📺 **Join our amazing History channel!** 📺 🌟\n\n"\
            "Friends, discover the magic of history through our engaging and thrilling channels! "\
            "Join us now to enjoy a wide range of programs and documentaries that will take you on an exciting journey "\
            "through the depths of history.\n\n"\
            "Experience ancient adventures, intriguing facts, and crucial events that shaped our world. "\
            "Join us today for a fun and enlightening educational experience!\n\n"\
            "🌍 Click the link to access the list of History channels: [@history_channels]"\

        bot.send_message(
            CHANNEL,
            message,
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error(
            'Error sending historical facts to the channel:', str(e))
