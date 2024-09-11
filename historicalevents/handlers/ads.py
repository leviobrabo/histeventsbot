import json
import random 
from datetime import datetime

from telebot import types

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger
from historicalevents.utils.get_historical import *


ads_links = [
    "https://www.cpmrevenuegate.com/aczkcs92r?key=bf57d0551edc1505d3b77aa5cda4bd66",
    "https://www.cpmrevenuegate.com/n4tz3iaax?key=2a5964f0ee7306247266e686b1cd3934"
]

def ads_message_channel_user(user_id):
    user = search_user(user_id)

    random_link = random.choice(ads_links)

    markup = types.InlineKeyboardMarkup()
    channel_ofc = types.InlineKeyboardButton(
            "ADS", url=random_link  
        )
    markup.add(channel_ofc)

    msg_text = "🔔 *Support our channel!* 🔔\n\n" \
           "Do you like the content? 🕰️📚 How about giving us a hand? By clicking on the ads, you help us keep bringing amazing stories every day, at no cost to you! 🚀✨\n\n" \
           "Each click makes a difference and helps us keep the channel active and up-to-date. 😊🙏\n\n" \
           "*Click and support the channel with just one tap!* 🙌"

    bot.send_message(
        user_id, msg_text, parse_mode="HTML", reply_markup=markup
    )


def ads_msg_job():
    try:
        user_models = get_all_users({"msg_private": "true"})
        for user_model in user_models:
            user_id = user_model["user_id"]
    
            ads_message_channel_user(user_id)

            logger.success(f"Message sent to user {user_id}")

        for channel_id in [CHANNEL, CHANNEL_POST]:
            random_link = random.choice(ads_links)
            markup = types.InlineKeyboardMarkup()
            channel_ofc = types.InlineKeyboardButton(
                "ADS", url=random_link
            )
            markup.add(channel_ofc)

            msg_text = "🔔 *Support our channel!* 🔔\n\n" \
                   "Do you like the content? 🕰️📚 How about giving us a hand? By clicking on the ads, you help us keep bringing amazing stories every day, at no cost to you! 🚀✨\n\n" \
                   "Each click makes a difference and helps us keep the channel active and up-to-date. 😊🙏\n\n" \
                   "*Click and support the channel with just one tap!* 🙌"

            bot.send_message(
                channel_id, msg_text, parse_mode="HTML", reply_markup=markup
            )

            logger.success(f"Message sent to channel {channel_id}")

    except Exception as e:
        logger.error("Error sending to users and channels:", str(e))


CHANNEL = int(config["FATOSHIST"]["HIST_CHANNEL"])
CHANNEL_IMG = int(config["FATOSHIST"]["CHANNEL_IMG"])
