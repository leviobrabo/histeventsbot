from telebot import types
import time

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger


@bot.message_handler(commands=['start'])
def cmd_start(message):
    try:
        if message.chat.type != 'private':
            return
        user_id = message.from_user.id
        user = search_user(user_id)
        first_name = message.from_user.first_name

        if not user:
            add_user_db(message)
            user = search_user(user_id)
            user_info = f"<b>#{BOT_USERNAME} #New_User</b>\n<b>User:</b> {user['first_name']}\n<b>ID:</b> <code>{user['user_id']}</code>\n<b>Username</b>: {user['username']}"
            bot.send_message(GROUP_LOG, user_info, message_thread_id=38558)

            logger.info(
                f'New user ID: {user["user_id"]} was created in the database'
            )

            return

        markup = types.InlineKeyboardMarkup()
        add_group = types.InlineKeyboardButton(
            '✨ Add me to your group',
            url='https://t.me/HistoricalEvents_bot?startgroup=true',
        )
        update_channel = types.InlineKeyboardButton(
            '⚙️ Bot updates', url='https://t.me/updatehist'
        )
        donate = types.InlineKeyboardButton(
            '💰 Donations', callback_data='donate'
        )
        channel_ofc = types.InlineKeyboardButton(
            'Official Channel 🇺🇸', url='https://t.me/today_in_historys'
        )
        how_to_use = types.InlineKeyboardButton(
            '⚠️ How to use the bot', callback_data='how_to_use'
        )
        config_pv = types.InlineKeyboardButton(
            '🪪 Your account', callback_data='config'
        )

        markup.add(add_group)
        markup.add(update_channel, channel_ofc)
        markup.add(donate, how_to_use)
        markup.add(config_pv)

        photo = 'https://i.imgur.com/8BCiwvz.png'
        msg_start = f"Hello, <b>{first_name}</b>!\n\nI am <b>Historical Events</b>, a bot that sends daily messages containing historical events that happened on the day of the message's delivery.\n\nSending messages in private chat is automatic. If you wish to stop receiving messages, type /sendoff. To start receiving again, type /sendon\n\n<b>The message is sent every day at 8 AM</b>\n\nAdd me to your group to receive the messages there.\n\n<b>Commands:</b> /help\n\n📦<b>My source code:</b> <a href='https://github.com/leviobrabo/historicaleventsbot'>GitHub</a>"

        bot.send_photo(
            message.chat.id,
            photo=photo,
            caption=msg_start,
            reply_markup=markup,
        )

    except Exception as e:
        bot.leave_chat(message.chat.id)
        logger.info(f'Bot left the group due to an error.')
        logger.error(f'Error while sending the start message: {e}')
        remove_chat_db(message.chat_id)

        logger.warning(
            f'Chat {message.chat_id} removed from the database due to an error while sending historical events message.'
        )
