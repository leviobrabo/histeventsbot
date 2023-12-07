import json
from datetime import datetime

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger


def send_poll(chat_id, question, options, correct_option_id, explanation):
    try:
        bot.send_poll(
            chat_id,
            question,
            options,
            is_anonymous=True,
            type='quiz',
            correct_option_id=correct_option_id,
            explanation=explanation[:200] if explanation else None,
        )
        logger.info('-' * 50)
        logger.success(f'Sent question to chat {chat_id}')
        logger.info('-' * 50)
    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Error sending the question: {e}')
        logger.info('-' * 50)


def send_question():
    try:
        today = datetime.now()
        current_time = today.time()

        with open(
            './historicalevents/data/question.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)

        events = json_events[f'{today.month}-{today.day}']

        if current_time.hour == 8 and current_time.minute == 30:
            send_poll(
                CHANNEL_POST,
                events['question1']['statement'],
                list(events['question1']['alternatives'].values()),
                list(events['question1']['alternatives']).index(
                    events['question1']['correct']
                ),
                events['question1'].get('explanation', ''),
            )

        elif current_time.hour == 12 and current_time.minute == 10:
            send_poll(
                CHANNEL_POST,
                events['question2']['statement'],
                list(events['question2']['alternatives'].values()),
                list(events['question2']['alternatives']).index(
                    events['question2']['correct']
                ),
                events['question2'].get('explanation', ''),
            )

        elif current_time.hour == 14 and current_time.minute == 0:
            send_poll(
                CHANNEL_POST,
                events['question3']['statement'],
                list(events['question3']['alternatives'].values()),
                list(events['question3']['alternatives']).index(
                    events['question3']['correct']
                ),
                events['question3'].get('explanation', ''),
            )

        elif current_time.hour == 18 and current_time.minute == 30:
            send_poll(
                CHANNEL_POST,
                events['question4']['statement'],
                list(events['question4']['alternatives'].values()),
                list(events['question4']['alternatives']).index(
                    events['question4']['correct']
                ),
                events['question4'].get('explanation', ''),
            )
    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Error sending the question: {e}')
        logger.info('-' * 50)
