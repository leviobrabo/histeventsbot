import json
from datetime import datetime

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger
from historicalevents.utils.get_historical import *
from historicalevents.utils.month import *


def get_history(CHANNEL):
    try:
        today = datetime.now()
        day = today.day
        month = today.month

        with open("./historicalevents/data/history.json", "r", encoding="utf-8") as file:
            json_events = json.load(file)
            historia = json_events.get(f"{month}-{day}", {})

            if historia:
                photo_url = historia.get("photo", "")
                caption = historia.get("text", "")

                if photo_url and caption:
                    message = (
                        f"<b>Narrated story 📰</b>\n\n"
                        f"<code>{caption}</code>\n\n"
                        f"<blockquote>💬 Did you know? Follow the @today_in_historys.</blockquote>"
                    )
                    bot.send_photo(CHANNEL, photo=photo_url, caption=message, parse_mode='HTML')
                else:
                    logger.info("Informações incompletas para o dia de hoje.")
                    warning_message = (
                        f"The story caption for the day {day}/{month} it's very long "
                        f"({len(caption)} characters). Please correct it so that it does not exceed 1024 characters."
                    )
                    bot.send_message(OWNER, warning_message)
            else:
                logger.info("There is no information for today.")
    
    except Exception as e:
        logger.error(f"Error getting information: {str(e)}", exc_info=True)

def hist_channel_history():
    try:
        get_history(CHANNEL)
        logger.success(f"Story sent to the channel {CHANNEL}")
    except Exception as e:
        logger.error(f"Error sending story: {str(e)}", exc_info=True)
