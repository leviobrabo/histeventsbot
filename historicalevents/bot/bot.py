import telebot

from historicalevents.config import TOKEN
from historicalevents.loggers import logger

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')
