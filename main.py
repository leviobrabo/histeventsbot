import threading
from time import sleep

import schedule
from telebot import util

from historicalevents.bot.bot import bot
from historicalevents.commands.admin import (cmd_addtopic, cmd_fwdoff,
                                             cmd_fwdon, cmd_remtopic)
from historicalevents.commands.help import cmd_help
from historicalevents.commands.photoshist import cmd_photo_hist
from historicalevents.commands.send import cmd_sendoff, cmd_sendon
from historicalevents.commands.start import cmd_start
from historicalevents.commands.sudo import (cmd_add_sudo, cmd_broadcast_chat,
                                            cmd_broadcast_pv, cmd_group,
                                            cmd_list_devs, cmd_rem_sudo,
                                            cmd_stats, cmd_sudo, cmd_sys)
from historicalevents.config import *
from historicalevents.core.poll_channel import *
from historicalevents.core.poll_chats import *
from historicalevents.database.db import *
from historicalevents.handlers.birth_of_day import *
from historicalevents.handlers.channel_creation_message import *
from historicalevents.handlers.christmas_message import *
from historicalevents.handlers.count_user_channel import *
from historicalevents.handlers.curiosity_channel import *
from historicalevents.handlers.death_of_day import *
from historicalevents.handlers.event_hist_channel import *
from historicalevents.handlers.event_hist_chats import *
from historicalevents.handlers.event_hist_users import *
from historicalevents.handlers.follow_channels import *
from historicalevents.handlers.holiday import *
from historicalevents.handlers.image_hist_events_channel import *
from historicalevents.handlers.image_hist_events_chat import *
from historicalevents.handlers.new_year_message import *
from historicalevents.handlers.prase_channel import *
from historicalevents.handlers.presidents import *
from historicalevents.loggers import logger
from historicalevents.utils.welcome import *
from historicalevents.version import *


def sudos(user_id):
    user = search_user(user_id)
    if user and user.get('sudo') == 'true':
        return True
    return False


def set_my_configs():
    try:
        bot.set_my_commands(
            [
                types.BotCommand('/start', 'Start'),
                types.BotCommand(
                    '/historicalphotos', 'Historical facts photos 🙂'
                ),
                types.BotCommand('/help', 'Help'),
                types.BotCommand(
                    '/sendon', 'You will receive the daily message at 8 AM'
                ),
                types.BotCommand(
                    '/sendoff',
                    'You will not receive the daily message at 8 AM',
                ),
            ],
            scope=types.BotCommandScopeAllPrivateChats(),
        )
    except Exception as ex:
        logger.error(ex)

    try:
        bot.set_my_commands(
            [
                types.BotCommand(
                    '/historicalphotos', 'Historical facts photos 🙂'
                ),
            ],
            scope=types.BotCommandScopeAllGroupChats(),
        )
    except Exception as ex:
        logger.error(ex)

    try:
        bot.set_my_commands(
            [
                types.BotCommand(
                    '/addtopic',
                    'Set a chat as a topic to receive daily messages',
                ),
                types.BotCommand(
                    '/remtopic',
                    'Remove a chat as a topic to receive daily messages (returns to General)',
                ),
                types.BotCommand('/fotoshist', 'Historical facts photos 🙂'),
                types.BotCommand('/fwd_on', 'Enable forwarding in the group'),
                types.BotCommand(
                    '/fwd_off', 'Disable forwarding in the group'
                ),
            ],
            scope=types.BotCommandScopeAllChatAdministrators(),
        )
    except Exception as ex:
        logger.error(ex)

    all_users = get_all_users()
    for user in all_users:
        if sudos(user.get('user_id')):
            try:
                bot.set_my_commands(
                    [
                        types.BotCommand('/sys', 'Server usage'),
                        types.BotCommand('/sudo', 'Elevate user'),
                        types.BotCommand('/ban', 'Ban user from the bot'),
                        types.BotCommand('/sudolist', 'List of sudo users'),
                        types.BotCommand('/banneds', 'List of banned users'),
                        types.BotCommand(
                            '/bcusers', 'Send broadcast message to users'
                        ),
                        types.BotCommand(
                            '/bcgps', 'Send broadcast message to groups'
                        ),
                    ],
                    scope=types.BotCommandScopeChat(
                        chat_id=user.get('user_id')
                    ),
                )
            except Exception as ex:
                logger.error(ex)



schedule.every().friday.at('22:30').do(message_CHANNEL_HISTORY_ALERT)

# Number of users on the channel
schedule.every(1).days.do(get_current_count)
# schedule.every().day.at('13:08').do(get_current_count)


# Poll sending to channel

schedule.every().day.at('08:30').do(send_question)
schedule.every().day.at('12:10').do(send_question)
schedule.every().day.at('14:00').do(send_question)
schedule.every().day.at('18:30').do(send_question)

# Poll sending to chats

schedule.every().day.at('10:30').do(send_question_chat)
schedule.every().day.at('14:30').do(send_question_chat)
schedule.every().day.at('16:30').do(send_question_chat)
schedule.every().day.at('21:30').do(send_question_chat)

# Remove polls from the database

# schedule.every().day.at('00:00').do(remove_all_poll)

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

# Sending Christmas messages

def check_dates_day():
    current_date = datetime.now()
    if current_date.month == 12 and current_date.day == 25:
        christmas_message()
    elif current_date.month == 1 and current_date.day == 1:
        new_year_message()
    elif current_date.month == 11 and current_date.day == 19:
        schedule_anniversary()

schedule.every().day.at('00:05').do(check_dates_day)



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
            msg_text = (
                "🤖 <b>How to use the Historical Events bot:</b>\n\n"
                "1️⃣ <b>/start</b> - Start interacting with the bot and receive a welcome message.\n"
                "2️⃣ <b>/help</b> - Get information on how to use the bot and see the available commands.\n"
                "3️⃣ <b>/fotoshist</b> - Sends historical photos.\n"
                "4️⃣ <b>/sendon</b> - To receive historical messages every day at 8 AM.\n"
                "5️⃣ <b>/sendoff</b> - To stop receiving historical messages every day at 8 AM.\n\n"
                "🌐 The bot works best in a channel or group, so add the bot to one for optimal learning.\n\n"
                "❇️ New features coming soon.\n\n"
                "📅 <b>Main Features:</b>\n"
                "- Receive daily historical facts.\n"
                "- Notifications for holidays and important events.\n"
                "- Personalized messages for special occasions.\n"
                "- Historical research and curiosities.\n\n"
                "🔧 <b>Utilities:</b> Anti-spam, historical data, automatic greetings, daily questions, and much more!"
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
        elif call.data.startswith('config'):
            user_id = call.from_user.id
            markup = types.InlineKeyboardMarkup()
            back_to_home = types.InlineKeyboardButton(
                '↩️ Back', callback_data='menu_start'
            )
            markup.add(back_to_home)

            user_info = search_user(user_id)
            if user_info:
                if 'hits' not in user_info:
                    user_info['hits'] = 0
                if 'questions' not in user_info:
                    user_info['questions'] = 0
                msg_text = f'<b>Your account</b>\n\n'
                msg_text += f'<b>Name:</b> {user_info["first_name"]}\n'
                if user_info.get('username'):
                    msg_text += f'<b>Username:</b> @{user_info["username"]}\n'
                msg_text += f'<b>Sudo:</b> {"Yes" if user_info["sudo"] == "true" else "No"}\n'
                msg_text += f'<b>Receives messages in private chat:</b>  {"Yes" if user_info["msg_private"] == "true" else "No"}\n'

                msg_text += f'<b>Correct Answers:</b> <code>{user_info["hits"]}</code>\n'
                msg_text += f'<b>Questions:</b> <code>{user_info["questions"]}</code>\n'

                if user_info['questions'] > 0:
                    percentage = (
                        user_info['hits'] / user_info['questions']
                    ) * 100
                    msg_text += f'<b>Percentage of correct answers per question:</b> <code>{percentage:.2f}%</code>\n'
                else:
                    msg_text += f'Percentage of correct answers per question: <code>0%</code>\n'
                photo = 'https://i.imgur.com/j3H3wvJ.png'
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
                '<b>List of commands</b>\n\n'
                '/fotoshist - Historical facts photos 🙂\n'
                '/sendon - You will receive the daily message at 8 AM\n'
                '/sendoff - You will not receive the daily message at 8 AM\n'
                '/fwd_off - Disable forwarding in the group\n'
                '/fwd_on - Enable forwarding in the group\n'
                '/addtopic - Set a chat as a topic to receive daily messages\n'
                '/remtpoic - Remove a chat as a topic to receive daily messages (returns to General)\n'
            )
            photo = 'https://i.imgur.com/j3H3wvJ.png'
            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                media=types.InputMediaPhoto(
                    media=photo, caption=msg_text, parse_mode='HTML'
                ),
                reply_markup=markup,
            )
        elif call.data.startswith('menu_help'):
            if call.message.chat.type != 'private':
                return
            user_id = call.message.from_user.id
            user = search_user(user_id)

            text = "Hello! I'm a bot programmed to send historical facts every day at predetermined times, starting at 8 am. \n\nMoreover, I have amazing commands that can be useful for you. Feel free to interact with me and discover more about the world around us! \n\n<b>Just click on one of them:</b>"

            markup = types.InlineKeyboardMarkup()
            commands = types.InlineKeyboardButton(
                'List of commands', callback_data='commands'
            )
            support = types.InlineKeyboardButton(
                'Support', url='https://t.me/updatehist'
            )
            donate = types.InlineKeyboardButton(
                '💰 Donate', url='https://t.me/updatehist'
            )

            markup.add(commands)
            markup.add(support, donate)

            photo = 'https://i.imgur.com/j3H3wvJ.png'
            bot.edit_message_media(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                media=types.InputMediaPhoto(
                    media=photo, caption=text, parse_mode='HTML'
                ),
                reply_markup=markup,
            )

    except Exception as e:
        logger.error(e)



def polling_thread():
    try:
        logger.success('Start polling...')
        bot.send_message(
            GROUP_LOG,
            f'#{BOT_NAME} #ONLINE\n\n<b>Bot is on</b>\n\n<b>Version:</b> {histevents_version}\n<b>Python version:</b> {python_version}\n<b>Lib version:</b> {telebot_version}',
            message_thread_id=38558,
        )
        bot.infinity_polling(allowed_updates=util.update_types)
    except Exception as e:
        logger.error(f"Error in polling_thread: {e}")
        bot.stop_polling()

def schedule_thread():
    try:
        while True:
            schedule.run_pending()
            sleep(1)
    except Exception as e:
        logger.error(f"Error in schedule_thread: {e}")


polling_thread = threading.Thread(target=polling_thread)
schedule_thread = threading.Thread(target=schedule_thread)

try:
    # set_my_configs()
    polling_thread.start()
    schedule_thread.start()
except Exception as e:
     logger.error(f"Error starting threads: {e}")




