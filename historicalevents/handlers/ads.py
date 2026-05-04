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
    "https://omg10.com/4/10930545",
    "https://omg10.com/4/10930547",
    "https://omg10.com/4/10930546",
    "https://omg10.com/4/10930523",
    "https://omg10.com/4/10963924",
    "https://omg10.com/4/10963927",
    "https://omg10.com/4/10963930",
    "https://omg10.com/4/10963933"
]

def ads_message_channel_user(user_id):
    user = search_user(user_id)

    random_link = random.choice(ads_links)

    markup = types.InlineKeyboardMarkup()
    channel_ofc = types.InlineKeyboardButton(
            "💰 GANHE DINHEIRO AGORA!", url=random_link
        )
    markup.add(channel_ofc)

    msg_text = "🎉 <b>You can earn money now!</b> 🎉\n\n" \
           "👆 Click the button below and earn extra cash! 💵\n\n" \
           "🔥 Don't miss this opportunity! Thousands are earning right now!\n\n" \
           "➡️ <b>Click here now and start earning!</b>"

    bot.send_message(
        user_id, msg_text, parse_mode="HTML", reply_markup=markup
    )


def ads_msg_job():
    try:
        user_models = get_all_users({"msg_private": "true"})
        for user_model in user_models:
            user_id = user_model["user_id"]

            for _ in range(2):
                ads_message_channel_user(user_id)
                logger.success(f"Message sent to user {user_id}")

        chat_models = get_all_chats()
        for chat_model in chat_models:
            chat_id = chat_model["chat_id"]

            random_link = random.choice(ads_links)
            markup = types.InlineKeyboardMarkup()
            channel_ofc = types.InlineKeyboardButton(
                "💰 EARN MONEY NOW!", url=random_link
            )
            markup.add(channel_ofc)

            msg_text = "🎉 <b>You can earn money now!</b> 🎉\n\n" \
                   "👆 Click the button below and earn extra cash! 💵\n\n" \
                   "🔥 Don't miss this opportunity! Thousands are earning right now!\n\n" \
                   "➡️ <b>Click here now and start earning!</b>"

            bot.send_message(
                chat_id, msg_text, parse_mode="HTML", reply_markup=markup
            )

            logger.success(f"Message sent to chat {chat_id}")

        for channel_id in [CHANNEL, CHANNEL_POST]:
            random_link = random.choice(ads_links)
            markup = types.InlineKeyboardMarkup()
            channel_ofc = types.InlineKeyboardButton(
                "💰 EARN MONEY NOW!", url=random_link
            )
            markup.add(channel_ofc)

            msg_text = "🎉 <b>You can earn money now!</b> 🎉\n\n" \
                   "👆 Click the button below and earn extra cash! 💵\n\n" \
                   "🔥 Don't miss this opportunity! Thousands are earning right now!\n\n" \
                   "➡️ <b>Click here now and start earning!</b>"

            bot.send_message(
                channel_id, msg_text, parse_mode="HTML", reply_markup=markup
            )

            logger.success(f"Message sent to channel {channel_id}")

    except Exception as e:
        logger.error("Error sending to users and channels:", str(e))
