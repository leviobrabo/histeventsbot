from sys import version_info

import telebot

python_version = f'{version_info[0]}.{version_info[1]}.{version_info[2]}'

telebot_version = telebot.__version__
