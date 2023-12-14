from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger
from historicalevents.utils.get_historical import *
from historicalevents.utils.month import *


def get_current_count():
    try:
        current_count = bot.get_chat_members_count(CHANNEL_POST)
        logger.info(f'Counter: {current_count}')
        current_date = datetime.now()

        last_entry = get_last_entry()

        if last_entry:
            difference_days = (current_date - last_entry['date']).days

            if difference_days >= 3:
                count_difference = current_count - last_entry['count']
                percentage_increase = (
                    ((count_difference) / last_entry['count']) * 100
                    if last_entry['count'] != 0
                    else 0
                )

                if count_difference > 0:
                    message = (
                        f'<b>Today in history, the number of members increased:</b>\n'
                        f"<b>Users before:</b> {last_entry['count']}\n"
                        f'<b>Users now:</b> {current_count}\n'
                        f'<b>Increase:</b> +{count_difference}\n'
                        f'<b>Percentage:</b> {percentage_increase:.2f}%'
                    )

                    bot.send_message(GROUP_LOG, message)
                    bot.send_message(OWNER, message)

                elif count_difference < 0:
                    message = (
                        f'<b>Today in history, the number of members decreased:</b>\n'
                        f"<b>Users before:</b> {last_entry['count']}\n"
                        f'<b>Users now:</b> {current_count}\n'
                        f'<b>Decrease:</b> -{abs(count_difference)}\n'
                        f'<b>Percentage:</b> {percentage_increase:.2f}%'
                    )

                    bot.send_message(GROUP_LOG, message)
                    bot.send_message(OWNER, message)
                else:
                    message = (
                        '<b>Today in history, the number of members remained the same.</b>\n'
                        f'<b>Users:</b> {current_count}'
                    )

                    bot.send_message(GROUP_LOG, message)
                    bot.send_message(OWNER, message)
        else:
            message = (
                '<b>This is the first check of the number of members:</b>\n'
                f'<b>Users:</b> {current_count}'
            )

            bot.send_message(GROUP_LOG, message)
            bot.send_message(OWNER, message)

        count_user_channel(current_count, current_date)
    except Exception as e:
        logger.error('Error getting information:', str(e))
