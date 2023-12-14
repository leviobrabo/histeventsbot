import json
from datetime import datetime, timedelta

import pytz

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger
from historicalevents.utils.get_historical import *
from historicalevents.utils.month import *

with open(
    './historicalevents/data/presidents.json', 'r', encoding='utf-8'
) as file:
    presidents = json.load(file)


def send_president_photo():
    try:
        if db.presidents.count_documents({}) == 0:
            president = presidents.get('1')
            new_id = 1
            new_date = datetime.now(
                pytz.timezone('America/Sao_Paulo')
            ).strftime('%Y-%m-%d')
            add_presidents_db(new_id, new_date)
            send_info_through_channel(president)
        else:
            last_president = (
                db.presidents.find().sort([('_id', -1)]).limit(1)[0]
            )
            last_id = last_president['id']
            sending_date = datetime.strptime(
                last_president['date'], '%Y-%m-%d'
            )

            next_id = int(last_id) + 1
            next_date = sending_date + timedelta(days=1)

            today = datetime.now(pytz.timezone('America/Sao_Paulo'))
            if next_date.date() == today.date():
                next_president = presidents.get(str(next_id))
                if next_president:
                    date = next_date.strftime('%Y-%m-%d')
                    add_presidents_db(next_id, date)

                    send_info_through_channel(next_president)
                else:

                    logger.error('No more presidents to send.')

            else:

                logger.info(
                    "It's not time yet to send information about the next president."
                )

    except Exception as e:

        logger.error(
            f'An error occurred while sending president information: {str(e)}'
        )


def send_info_through_channel(president_info):
    try:
        title = president_info.get('title', '')
        name = president_info.get('name', '')
        position = president_info.get('position', '')
        party = president_info.get('party', '')
        term_year = president_info.get('term_year', '')
        vice_president = president_info.get('vice_president', '')
        photo = president_info.get('photo', '')

        caption = (
            f'<b>{title}</b>\n\n'
            f'<b>Name:</b> {name}\n'
            f'<b>Information:</b> {position}° {title}\n'
            f'<b>Party:</b> {party}\n'
            f'<b>Term Year:</b> {term_year}\n'
            f'<b>Vice-President:</b> {vice_president}\n\n'
            f'💬 Did you know? Follow @today_in_historys.'
        )

        logger.success('President sending completed successfully!')

        bot.send_photo(
            CHANNEL, photo=photo, caption=caption, parse_mode='HTML'
        )
    except Exception as e:

        logger.error(f'Error sending president photo: {str(e)}')
