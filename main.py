import threading
from time import sleep

import schedule
from telebot import util

from historicalevents.bot.bot import bot
from historicalevents.commands.admin import (
    commands_fwdoff,
    commands_fwdon,
    commands_settopic,
    commands_unsettopic,
)
from historicalevents.commands.photoshist import fotos_hist
from historicalevents.commands.help import cmd_help
from historicalevents.commands.send import commands_sendff, commands_sendon
from historicalevents.commands.start import cmd_start
from historicalevents.commands.sudo import (
    add_sudo,
    commands_sudo,
    grupos,
    handle_broadcast_chat,
    handle_broadcast_pv,
    list_devs,
    stats,
    unsudo_command,
)
from historicalevents.config import *
from historicalevents.core.poll_channel import *
from historicalevents.core.poll_chats import *
from historicalevents.database.db import *
from historicalevents.handlers.birth_of_day import *
from historicalevents.handlers.curiosity_channel import *
from historicalevents.handlers.death_of_day import *
from historicalevents.handlers.event_hist_channel import *
from historicalevents.handlers.event_hist_chats import *
from historicalevents.handlers.event_hist_users import *
from historicalevents.handlers.holiday import *
from historicalevents.handlers.image_hist_events_channel import *
from historicalevents.handlers.image_hist_events_chat import *
from historicalevents.handlers.prase_channel import *
from historicalevents.handlers.presidents import *
from historicalevents.loggers import logger
from historicalevents.utils.welcome import *

bot.add_message_handler(cmd_start)
bot.add_message_handler(cmd_help)
bot.add_message_handler(add_sudo)
bot.add_message_handler(unsudo_command)
bot.add_message_handler(grupos)
bot.add_message_handler(stats)
bot.add_message_handler(handle_broadcast_pv)
bot.add_message_handler(handle_broadcast_chat)
bot.add_message_handler(list_devs)
bot.add_message_handler(commands_sudo)
bot.add_message_handler(commands_sendon)
bot.add_message_handler(commands_sendff)
bot.add_message_handler(commands_fwdon)
bot.add_message_handler(commands_fwdoff)
bot.add_message_handler(commands_settopic)
bot.add_message_handler(commands_unsettopic)


def sudos(user_id):
    user = search_user(user_id)
    if user and user.get('sudo') == 'true':
        return True
    return False


def set_my_configs():
    try:
        bot.set_my_commands(
            [
                types.BotCommand('/start', 'start'),
                types.BotCommand('/help', 'help'),
            ],
            scope=types.BotCommandScopeAllPrivateChats(),
        )
    except Exception as ex:
        logger.error(ex)

    for sudo in sudos:
        try:
            bot.set_my_commands(
                [
                    types.BotCommand('/sys', 'Server usage'),
                    types.BotCommand('/sudo', 'Elevate user'),
                    types.BotCommand('/ban', 'Ban user from bot'),
                    types.BotCommand('/sudolist', 'List of sudo users'),
                    types.BotCommand('/banneds', 'List of banned users'),
                    types.BotCommand(
                        '/bcusers', 'Send broadcast message to users'
                    ),
                    types.BotCommand(
                        '/bcgps', 'Send broadcast message to groups'
                    ),
                ],
                scope=types.BotCommandScopeChat(chat_id=sudo),
            )

        except Exception as ex:
            logger.error(ex)

    try:
        bot.set_my_commands(
            [
                types.BotCommand('/start', 'start'),
                types.BotCommand('/help', 'help'),
            ],
            scope=types.BotCommandScopeAllGroupChats(),
        )
    except Exception as ex:
        logger.error(ex)

    try:
        bot.set_my_commands(
            [
                types.BotCommand('/start', 'start'),
                types.BotCommand('/help', 'help'),
            ],
            scope=types.BotCommandScopeChatAdministrators(),
        )
    except Exception as ex:
        logger.error(ex)


# Poll sending to channel

schedule.every().day.at('08:30').do(send_question)
schedule.every().day.at('11:30').do(send_question)
schedule.every().day.at('14:00').do(send_question)
schedule.every().day.at('18:30').do(send_question)

# Poll sending to chats

schedule.every().day.at('10:30').do(send_question_chat)
schedule.every().day.at('14:30').do(send_question_chat)
schedule.every().day.at('16:30').do(send_question_chat)
schedule.every().day.at('21:30').do(send_question_chat)

# Remove polls from the database

schedule.every().day.at('00:00').do(remove_all_poll)

# Sending historical events in chats

schedule.every().day.at('08:00').do(hist_chat_job)

# Sending historical events to users

schedule.every().day.at('08:30').do(hist_user_job)

# Sending historical events to the channel

schedule.every().day.at('05:00').do(hist_channel)

# Sending deaths of the day to the channel

schedule.every().day.at('15:30').do(hist_channel_death)

# Sending births of the day to the channel

schedule.every().day.at('01:00').do(hist_channel_birth)

# Sending holidays of the day to the channel

schedule.every().day.at('00:00').do(hist_channel_holiday)

# Sending historical photos to the group

schedule.every().day.at('15:00').do(hist_image_chat_job)

# Sending historical photos to the channel

schedule.every().day.at('17:00').do(hist_channel_imgs)

# Sending curiosities to the channel

schedule.every().day.at('10:00').do(hist_channel_curiosity)

# Sending quotes to the channel

schedule.every().day.at('21:30').do(hist_channel_quote)

# Sending presidents to the channel

schedule.every().day.at('20:00').do(send_president_photo)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        if call.data.startswith('menu_start'):
            if call.message.chat.type != 'private':
                return
            user_id = call.from_user.id
            first_name = call.from_user.first_name
            user = search_user(user_id)

            if not user:
                add_user_db(call.message)
                user = search_user(user_id)
                user_info = f"<b>#{BOT_USERNAME} #New_User</b>\n<b>User:</b> {user['first_name']}\n<b>ID:</b> <code>{user['user_id']}</code>\n<b>Username</b>: {user['username']}"
                bot.send_message(GROUP_LOG, user_info)

            markup = types.InlineKeyboardMarkup()
            add_group = types.InlineKeyboardButton(
                '✨ Add me to your group',
                url='https://t.me/HistoricalEvents_bot?startgroup=true',
            )
            update_channel = types.InlineKeyboardButton(
                '⚙️ Bot Updates', url='https://t.me/updatehist'
            )
            donate = types.InlineKeyboardButton(
                '💰 Donations', callback_data='donate'
            )
            channel_ofc = types.InlineKeyboardButton(
                'Official Channel 🇧🇷', url='https://t.me/today_in_historys'
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
            msg_start = f"Hello, <b>{first_name}</b>!\n\nI'm <b>Historical Facts</b>, a bot that sends daily messages with historical events that occurred on the day the message was sent.\n\nThe message is sent automatically in private chats. If you want to stop receiving it, type /sendoff. To start receiving again, type /sendon\n\n<b>The message is sent every day at 8 am</b>\n\nAdd me to your group to receive messages there.\n\n<b>Commands:</b> /help\n\n📦<b>My source code:</b> <a href='https://github.com/leviobrabo/historicalevents'>GitHub</a>"

            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                media=types.InputMediaPhoto(
                    media=photo, caption=msg_start, parse_mode='HTML'
                ),
                reply_markup=markup,
            )

        elif call.data.startswith('donate'):
            user_id = call.from_user.id
            markup = types.InlineKeyboardMarkup()
            back_to_home = types.InlineKeyboardButton(
                '↩️ Back', callback_data='menu_start'
            )
            markup.add(back_to_home)
            text_msg = (
                '──❑ D 「 🤝 Donation 」❑──\n\n'
                ' ☆ <b>BTC:</b>\n <code>bc1qjxzlug0cwnfjrhacy9kkpdzxfj0mcxc079axtl</code>\n\n'
                ' ☆ <b>ETH/USDT:</b>\n <code>0x1fbde0d2a96869299049f4f6f78fbd789d167d1b</code>'
            )

            photo = 'https://i.imgur.com/8BCiwvz.png'
            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                media=types.InputMediaPhoto(
                    media=photo, caption=text_msg, parse_mode='HTML'
                ),
                reply_markup=markup,
            )
        elif call.data.startswith('how_to_use'):
            user_id = call.from_user.id
            markup = types.InlineKeyboardMarkup()
            back_to_home = types.InlineKeyboardButton(
                '↩️ Back', callback_data='menu_start'
            )
            markup.add(back_to_home)
            msg_text = 'how to use the bot'
            photo = 'https://i.imgur.com/8BCiwvz.png'
            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                media=types.InputMediaPhoto(
                    media=photo, caption=msg_text, parse_mode='HTML'
                ),
                reply_markup=markup,
            )
        elif call.data.startswith('config'):
            user_id = call.from_user.id
            markup = types.InlineKeyboardMarkup()
            back_to_home = types.InlineKeyboardButton(
                '↩️ Back', callback_data='menu_start'
            )
            markup.add(back_to_home)
            msg_text = 'Your account'
            photo = 'https://i.imgur.com/8BCiwvz.png'
            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                media=types.InputMediaPhoto(
                    media=photo, caption=msg_text, parse_mode='HTML'
                ),
                reply_markup=markup,
            )
        elif call.data.startswith('commands'):
            user_id = call.from_user.id
            markup = types.InlineKeyboardMarkup()
            back_to_home = types.InlineKeyboardButton(
                '↩️ Back', callback_data='menu_help'
            )
            markup.add(back_to_home)
            msg_text = (
                '<b>Command list</b>\n\n'
                '/fotoshist - Photos of historical facts 🙂\n'
                '/sendon - Receive the daily message at 8 am\n'
                '/sendoff - Do not receive the daily message at 8 am\n'
                '/fwdoff - Disable forwarding in the group\n'
                '/fwdon - Enable forwarding in the group\n'
                '/settopic - Set a chat as a topic to receive daily messages\n'
                '/cleartopic - Remove a chat as a topic to receive daily messages (returns to General)\n'
            )
            photo = 'https://i.imgur.com/8BCiwvz.png'
            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                media=types.InputMediaPhoto(
                    media=photo, caption=msg_text, parse_mode='HTML'
                ),
                reply_markup=markup,
            )

    except Exception as e:
        logger.error(e)


def polling_thread():
    logger.info('-' * 50)
    logger.success('Start polling...')
    logger.info('-' * 50)
    bot.infinity_polling(allowed_updates=util.update_types, skip_pending=True)


def schedule_thread():
    while True:
        schedule.run_pending()

        sleep(1)


polling_thread = threading.Thread(target=polling_thread)
schedule_thread = threading.Thread(target=schedule_thread)

polling_thread.start()
schedule_thread.start()

try:
    polling_thread.join()
    schedule_thread.join()
except Exception as e:
    pass
