import json
from datetime import datetime

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger


def send_poll_chat(
    chat_id,
    question,
    options,
    correct_option_id,
    explanation,
    message_thread_id,
):
    try:
        today = datetime.now()
        current_date = today.strftime('%d/%m/%Y')

        chat_info = bot.get_chat(chat_id)
        chat_type = chat_info.type

        is_anonymous = True if chat_type == 'channel' else False

        sent_poll = bot.send_poll(
            chat_id,
            question,
            options,
            is_anonymous=is_anonymous,
            type='quiz',
            correct_option_id=correct_option_id,
            explanation=explanation[:200] if explanation else None,
            message_thread_id=message_thread_id,
        )

        poll_id = sent_poll.poll.id

        add_poll_db(chat_id, poll_id, correct_option_id, current_date)

        logger.success(f'Sent question to chat {chat_id}')

    except Exception as e:

        logger.error(f'Error sending the question: {e}')


def send_question_chat():
    try:
        today = datetime.now()
        current_time = today.time()

        with open(
            './historicalevents/data/question.json', 'r', encoding='utf-8'
        ) as file:
            json_events = json.load(file)

        events = json_events[f'{today.month}-{today.day}']

        all_chats = get_all_chats({'forwarding': 'true'})

        for chat in all_chats:
            chat_id = chat['chat_id']
            chat_db = search_group(chat_id)
            thread_id = chat_db.get('thread_id')
            if chat_id and chat_id != '':
                if current_time.hour == 10 and current_time.minute == 30:
                    send_poll_chat(
                        chat_id,
                        events['question1']['statement'],
                        list(events['question1']['alternatives'].values()),
                        list(events['question1']['alternatives']).index(
                            events['question1']['correct']
                        ),
                        events['question1'].get('explanation', ''),
                        thread_id,
                    )

                elif current_time.hour == 14 and current_time.minute == 30:
                    send_poll_chat(
                        chat_id,
                        events['question2']['statement'],
                        list(events['question2']['alternatives'].values()),
                        list(events['question2']['alternatives']).index(
                            events['question2']['correct']
                        ),
                        events['question2'].get('explanation', ''),
                        thread_id,
                    )

                elif current_time.hour == 16 and current_time.minute == 30:
                    send_poll_chat(
                        chat_id,
                        events['question3']['statement'],
                        list(events['question3']['alternatives'].values()),
                        list(events['question3']['alternatives']).index(
                            events['question3']['correct']
                        ),
                        events['question3'].get('explanation', ''),
                        thread_id,
                    )

                elif current_time.hour == 21 and current_time.minute == 30:
                    send_poll_chat(
                        chat_id,
                        events['question4']['statement'],
                        list(events['question4']['alternatives'].values()),
                        list(events['question4']['alternatives']).index(
                            events['question4']['correct']
                        ),
                        events['question4'].get('explanation', ''),
                        thread_id,
                    )

    except Exception as e:

        logger.error(f'Error sending the question: {e}')


@bot.poll_answer_handler()
def handle_poll_answer(poll_answer):
    try:
        user_id = poll_answer.user.id
        first_name = poll_answer.user.first_name
        last_name = poll_answer.user.last_name
        username = poll_answer.user.username

        poll_id = poll_answer.poll_id
        option_id = poll_answer.option_ids[0]

        poll_db = search_poll(poll_id)
        correct_option = poll_db.get('correct_option_id')

        user = search_user(user_id)
        if not user:
            add_new_user(user_id, first_name, last_name, username)

        if option_id == correct_option:
            set_hit_user(user_id)
            set_questions_user(user_id)

    except Exception as e:

        logger.error(f'Error processing poll answer: {e}')


def remove_all_poll():
    try:
        logger.success('Removed polls from the database!')
        remove_all_poll_db()
    except Exception as e:

        logger.error(f'Error processing poll answer: {e}')
