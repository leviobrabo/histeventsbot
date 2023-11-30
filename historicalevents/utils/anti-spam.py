from time import sleep

from telebot.apihelper import ApiTelegramException

from historicalevents.bot.bot import bot

for _ in range(4):
    try:
        bot.send_message
    except ApiTelegramException as ex:
        if ex.error_code == 429:
            sleep(ex.result_json['parameters']['retry_after'])
        else:
            raise
else:
    bot.send_message
