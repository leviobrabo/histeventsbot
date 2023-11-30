import configparser
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
bot_conf_path = os.path.join(script_directory, '..', 'bot.conf')

config = configparser.ConfigParser()
config.read(bot_conf_path)

TOKEN = config['HISTORICALEVENTS']['TOKEN']
GROUP_LOG = int(config['HISTORICALEVENTS']['HIST_LOG'])
CHANNEL = int(config['HISTORICALEVENTS']['HIST_CHANNEL'])
BOT_NAME = config['HISTORICALEVENTS']['BOT_NAME']
BOT_USERNAME = config['HISTORICALEVENTS']['BOT_USERNAME']
OWNER = int(config['HISTORICALEVENTS']['OWNER_ID'])
CHANNEL_POST = int(config['HISTORICALEVENTS']['HIST_CHANNEL_POST'])
LOG_PATH = config['LOG']['LOG_PATH']
MONGO_CON = config['DB']['MONGO_CON']
