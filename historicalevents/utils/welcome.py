from telebot import types
from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger


def send_new_group_message(chat):
    try:
        chatusername = (
            f'@{chat.username}' if chat.username else 'Private Group'
        )
        bot.send_message(
            GROUP_LOG,
            text=f'#{BOT_USERNAME} #New_Group\n'
            f'<b>Chat:</b> {chat.title}\n'
            f'<b>ID:</b> <code>{chat.id}</code>\n'
            f'<b>Link:</b> {chatusername}',
            parse_mode='html',
            disable_web_page_preview=True,
        )
    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Error adding group to the database: {e}')
        logger.info('-' * 50)


@bot.my_chat_member_handler()
def send_group_greeting(message: types.ChatMemberUpdated):
    try:
        old_member = message.old_chat_member
        new_member = message.new_chat_member
        if message.chat.type != 'private' and new_member.status in [
            'member',
            'administrator',
        ]:
            chat_id = message.chat.id
            chat_name = message.chat.title

            if chat_id == CHANNEL:
                logger.info('-' * 50)
                logger.warning(
                    f'Ignoring storage of chat with ID {chat_id}, as it matches the configured channel ID.'
                )
                logger.info('-' * 50)
                return

            if chat_id == CHANNEL_POST:
                logger.info('-' * 50)
                logger.warning(
                    f'Ignoring storage of chat with ID {chat_id}, as it matches the configured channel ID.'
                )
                logger.info('-' * 50)
                return

            if chat_id == GROUP_LOG:
                logger.info('-' * 50)
                logger.warning(
                    f'Ignoring storage of chat with ID {chat_id}, as it matches the configured channel ID.'
                )
                logger.info('-' * 50)
                return

            existing_chat = search_group(chat_id)
            if existing_chat:
                logger.info('-' * 50)
                logger.warning(
                    f'Chat with ID {chat_id} already exists in the database.'
                )
                logger.info('-' * 50)
                return

            add_chat_db(chat_id, chat_name)
            logger.info('-' * 50)
            logger.success(
                f'⭐️ The bot has been added to the group {chat_name} - ({chat_id})'
            )
            logger.info('-' * 50)
            send_new_group_message(message.chat)

            if message.chat.type in ['group', 'supergroup', 'channel']:
                markup = types.InlineKeyboardMarkup()
                channel_ofc = types.InlineKeyboardButton(
                    'Official Channel 🇧🇷', url='https://t.me/today_in_historys'
                )
                report_bugs = types.InlineKeyboardButton(
                    'Report Bugs', url='https://t.me/kylorensbot'
                )
                markup.add(channel_ofc, report_bugs)
                bot.send_message(
                    chat_id,
                    'Hello, my name is <b>Historical events</b>! Thank you for adding me to your group.\n\nI will send messages every day at 8 AM and I have some commands.\n\nIf you want to receive more historical facts, grant me administrator permissions to pin messages and invite users via link.',
                    reply_markup=markup,
                )
    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Error handling group greeting: {e}')
        logger.info('-' * 50)


@bot.message_handler(content_types=['left_chat_member'])
def on_left_chat_member(message):
    try:
        if message.left_chat_member.id == bot.get_me().id:
            chat_id = message.chat.id
            chat_name = message.chat.title
            remove_chat_db(chat_id)
            logger.success(
                f'The bot has been removed from the group {chat_name} - ({chat_id})'
            )
    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Error removing group from the database: {e}')
        logger.info('-' * 50)
