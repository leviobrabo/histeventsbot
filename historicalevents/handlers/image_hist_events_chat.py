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


def send_historical_events_group_image(chat_id):
    try:
        today = datetime.now(pytz.timezone('America/Sao_Paulo'))
        day = today.day
        month = today.month

        response = requests.get(
            f'https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}'
        )
        events = response.json().get('events', [])

        if events:
            random_event = random.choice(events)
            event_text = random_event.get('text', '')
            event_year = random_event.get('year', '')

            caption = f'<b>Did you know?</b>\n\nOn <b>{day} of {get_month_name(month)} {event_year}</b>\n\n<code>{event_text}</code>'
            inline_keyboard = types.InlineKeyboardMarkup()
            inline_keyboard.add(
                types.InlineKeyboardButton(
                    text='📢 Official Channel', url='https://t.me/today_in_historys'
                )
            )

            if random_event.get('pages') and random_event['pages'][0].get(
                'thumbnail'
            ):
                photo_url = random_event['pages'][0]['thumbnail']['source']
                bot.send_photo(
                    chat_id,
                    photo_url,
                    caption,
                    parse_mode='HTML',
                    reply_markup=inline_keyboard,
                )
            else:
                bot.send_message(
                    chat_id,
                    caption,
                    parse_mode='HTML',
                    reply_markup=inline_keyboard,
                )
            logger.info('-' * 50)
            logger.success(
                f'Historical event in photo sent successfully to chat ID {chat_id}.'
            )
            logger.info('-' * 50)
        else:
            logger.info('-' * 50)
            logger.info('There are no historical events for the current day.')
            logger.info('-' * 50)
    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Failed to send historical event: {e}')
        logger.info('-' * 50)


def hist_image_chat_job():
    try:
        chat_models = get_all_chats({'forwarding': 'true'})
        for chat_model in chat_models:
            chat_id = chat_model['chat_id']
            if chat_id != GROUP_LOG:
                try:
                    send_historical_events_group_image(chat_id)
                except Exception as e:
                    logger.info('-' * 50)
                    logger.error(
                        f'Error sending image historical events to group {chat_id}: {str(e)}'
                    )
                    logger.info('-' * 50)
    except Exception as e:
        logger.info('-' * 50)
        logger.error('Error sending images to chats:', str(e))
        logger.info('-' * 50)
