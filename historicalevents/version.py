from sys import version_info

import telebot

python_version = f'{version_info[0]}.{version_info[1]}.{version_info[2]}'
histevents_version = '3.2.9'
telebot_version = (
    telebot.__version__
    if hasattr(telebot, '__version__')
    else 'Version not found'
)
