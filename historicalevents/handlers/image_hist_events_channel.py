import random
from datetime import datetime

import pytz
import requests
from telebot import types

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger
from historicalevents.utils.get_historical import *
from historicalevents.utils.month import *


def send_historical_events_channel_image(CHANNEL):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}'
        )
        events = response.json().get('events', [])
        events_with_photo = [
            event
            for event in events
            if event.get('pages') and event['pages'][0].get('thumbnail')
        ]

        if events_with_photo:
            random_event = random.choice(events_with_photo)
            event_text = random_event.get('text', '')
            event_year = random_event.get('year', '')

            caption = f'<b>🖼 | Illustrated History </b>\n\nOn <b>{day} of {get_month_name(month)} {event_year}</b>\n\n<code>{event_text}</code>\n\n💬 Did you know? Follow @today_in_historys.'

            options = {'parse_mode': 'HTML'}

            photo_url = random_event['pages'][0]['thumbnail']['source']
            bot.send_photo(CHANNEL, photo_url, caption=caption, **options)

            logger.success(
                f'Historical event in photo sent successfully to channel ID {CHANNEL}.'
            )
        else:
            logger.info('There are no events with photos to send today.')

    except Exception as e:
        logger.error(f'Failed to send historical event: {e}')


def hist_channel_imgs():
    try:
        send_historical_events_channel_image(CHANNEL)
        logger.success(f'Message sent to channel {CHANNEL}')

    except Exception as e:
        logger.error('Error sending image job:', str(e))
