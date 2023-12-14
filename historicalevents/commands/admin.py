from telebot import types

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger


@bot.message_handler(commands=['fwdoff'])
def cmd_fwdoff(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        chat_name = message.chat.title
        chat_type = message.chat.type
        chat_member = bot.get_chat_member(chat_id, user_id)

        if chat_type in ['group', 'supergroup', 'channel']:
            if chat_member.status not in ('administrator', 'creator'):
                bot.reply_to(
                    message,
                    'You need to be an administrator to perform this action.',
                )
                return

            existing_chat = search_group(chat_id)
            if not existing_chat:
                add_chat_db(chat_id, chat_name)
                send_new_group_message(message.chat)
                return

            if existing_chat.get('forwarding') == 'false':
                bot.reply_to(
                    message,
                    f'Notifications for {chat_name} are already disabled.',
                )
                return

        update_forwarding_status(chat_id, 'false')
        markup = types.InlineKeyboardMarkup()
        report_bugs = types.InlineKeyboardButton(
            'Report bugs', url='https://t.me/kylorensbot'
        )
        markup.add(report_bugs)
        bot.reply_to(
            message,
            '<b>Forwarding has been successfully DISABLED</b>.\n\nFrom now on...\n\nThe chat will only receive historical facts messages for the day.',
            reply_markup=markup,
        )
        bot.send_message(
            GROUP_LOG,
            f'<b>#{BOT_USERNAME} #Fwdoff</b>\n\<b>Chat</b>: {chat_name}\n<b>ID:</b> <code>{chat_id}</code>',
        )

    except Exception as e:

        logger.error(f'Error disabling chat forwarding: {str(e)}')


@bot.message_handler(commands=['fwdon'])
def cmd_fwdon(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        chat_name = message.chat.title
        chat_type = message.chat.type
        chat_member = bot.get_chat_member(chat_id, user_id)

        if chat_type in ['group', 'supergroup', 'channel']:
            if chat_member.status not in ('administrator', 'creator'):
                bot.reply_to(
                    message,
                    'You need to be an administrator to perform this action.',
                )
                return

            existing_chat = search_group(chat_id)
            if not existing_chat:
                add_chat_db(chat_id, chat_name)
                send_new_group_message(message.chat)
                return

            if existing_chat.get('forwarding') == 'true':
                bot.reply_to(
                    message,
                    f'Notifications for {chat_name} are already enabled.',
                )
                return

        update_forwarding_status(chat_id, 'true')
        markup = types.InlineKeyboardMarkup()
        report_bugs = types.InlineKeyboardButton(
            'Report bugs', url='https://t.me/kylorensbot'
        )
        markup.add(report_bugs)
        bot.reply_to(
            message,
            '<b>Forwarding has been successfully ENABLED.</b>\n\nFrom now on...\n\nThe chat will receive historical facts messages for the day and historical forwards.',
            reply_markup=markup,
        )
        bot.send_message(
            GROUP_LOG,
            f'<b>#{BOT_USERNAME} #Fwdon</b>\n\<b>Chat</b>: {chat_name}\n<b>ID:</b> <code>{chat_id}</code>',
        )
    except Exception as e:

        logger.error(f'Error enabling chat forwarding: {str(e)}')


@bot.message_handler(commands=['settopic'])
def cmd_settopic(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        chat_type = message.chat.type
        chat_member = bot.get_chat_member(chat_id, user_id)

        if (
            message.reply_to_message
            and message.reply_to_message.message_thread_id
        ):
            thread_id = message.reply_to_message.message_thread_id
        else:
            bot.reply_to(
                message,
                'This command must be a reply to a message with a thread_id.',
            )
            return

        if chat_type in ['group', 'supergroup']:
            if chat_member.status not in ('creator'):
                bot.reply_to(
                    message,
                    'You need to be the chat owner to perform this action.',
                )
                return

            update_thread_id(chat_id, thread_id)

            bot.reply_to(
                message,
                f'The Topic was successfully updated!\n\nThread_id= {thread_id}\n\nYou will now receive historical facts here.',
            )

    except Exception as e:

        logger.error(f'Error setting the topic: {str(e)}')


# unsettopic


@bot.message_handler(commands=['unsettopic'])
def cmd_unsettopic(message):
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        chat_type = message.chat.type
        chat_member = bot.get_chat_member(chat_id, user_id)

        if chat_type in ['group', 'supergroup']:
            if chat_member.status not in ('creator'):
                bot.reply_to(
                    message,
                    'You need to be the chat owner to perform this action.',
                )
                return

            update_thread_id(chat_id, '')

            bot.reply_to(
                message,
                'The messages sent in the topic have been successfully removed!',
            )

    except Exception as e:

        logger.error(f'Error removing the topic: {str(e)}')


def send_new_group_message(chat):
    if chat.username:
        chatusername = f'@{chat.username}'
    else:
        chatusername = 'Private Group'
    bot.send_message(
        GROUP_LOG,
        text=f'#{BOT_USERNAME} #New_Group\n'
        f'<b>Chat:</b> {chat.title}\n'
        f'<b>ID:</b> <code>{chat.id}</code>\n'
        f'<b>Link:</b> {chatusername}',
        parse_mode='html',
        disable_web_page_preview=True,
    )
