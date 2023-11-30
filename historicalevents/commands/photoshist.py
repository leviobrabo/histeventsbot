import random

from historicalevents.bot.bot import bot
from historicalevents.config import *
from historicalevents.database.db import *
from historicalevents.loggers import logger

historicals = [
    {
        'title': 'Police officer scolding a man in San Francisco, USA, for not wearing a mask during the 1918 Flu pandemic © California State Library',
        'image': 'https://i.imgur.com/8Q9OC3d.jpeg',
    },
    {
        'title': 'Family and friends visiting quarantined patients at Ullevål Hospital in Oslo, Norway, in 1905 © Anders Beer Wilse',
        'image': 'https://i.imgur.com/ifSFlsp.jpeg',
    },
    {
        'title': 'Celebration for the liberation of the Auschwitz concentration camp in Poland by the Soviet army in 1945',
        'image': 'https://i.imgur.com/ksdeCm1.png',
    },
    {
        'title': 'Survivors of the famous plane crash in the Andes in 1972, where people had to resort to cannibalism to survive for 72 days in the snow',
        'image': 'https://i.imgur.com/eIZC0yH.png',
    },
    {
        'title': 'Michelangelo\'s David statue covered by a brick protection to prevent damage from bombings during World War II',
        'image': 'https://i.imgur.com/PgMKq6S.png',
    },
    {
        'title': 'Famous beachfront house in San Francisco, USA, in 1907, shortly before being destroyed by fire',
        'image': 'https://i.imgur.com/E3rAaKZ.png',
    },
    {
        'title': 'Historic photo of Princess Diana shaking hands with an AIDS patient without gloves in 1991, at a time when prejudice and ignorance still influenced notions about the disease\'s transmission',
        'image': 'https://i.imgur.com/LdsE0TS.png',
    },
    {
        'title': '“Selfie” taken by Czar Nicholas II of Russia before the revolution',
        'image': 'https://i.imgur.com/hBEu5tk.png',
    },
    {
        'title': 'Gaspar Wallnöfer, at 79 years old in 1917, the oldest Australian soldier during World War I, who had already fought in battles in Italy in 1848 and 1866',
        'image': 'https://i.imgur.com/nYdyTjF.png',
    },
    {
        'title': '“Night Witches”, group of Russian female pilots who bombed the Nazis in nighttime attacks in 1941',
        'image': 'https://i.imgur.com/nK0ydXb.png',
    },
    {
        'title': 'Las Vegas police officers facing Mike Tyson moments after the boxer bit off part of his opponent, Evander Holyfield\'s ear, in 1996',
        'image': 'https://i.imgur.com/Dw075SY.png',
    },
    {
        'title': 'Young Bill Clinton shaking hands with then-President John Kennedy at the White House in 1963',
        'image': 'https://i.imgur.com/MwC2K0h.png',
    },
    {
        'title': 'Workers atop the North Tower of the World Trade Center in New York in 1973',
        'image': 'https://i.imgur.com/kUy0V52.png',
    },
    {
        'title': 'Before and after World War of Soviet soldier Eugen Stepanovich Kobytev: on the left, in 1941, the day he went to war, and on the right, in 1945, at the end of the conflict',
        'image': 'https://i.imgur.com/RnjY0za.png',
    },
    {
        'title': 'British soldier with his young daughter returning home in 1945',
        'image': 'https://i.imgur.com/EoX9JIB.png',
    },
    {
        'title': 'Cetshwayo, King of the Zulus, who defeated the British army at the Battle of Isandlwana in 1878',
        'image': 'https://i.imgur.com/DedYfRB.png',
    },
    {
        'title': 'Anti-British propaganda in Japan in 1941',
        'image': 'https://i.imgur.com/WFmfZBF.png',
    },
    {
        'title': 'Undercover police officer on duty in New York in 1969',
        'image': 'https://i.imgur.com/w0sAgsN.png',
    },
    {
        'title': 'Acrobats atop the Empire State Building in New York in 1934',
        'image': 'https://i.imgur.com/1COKRBn.png',
    },
    {
        'title': 'Road crossing the snow in the Pyrenees Mountains, in the French part, in 1956',
        'image': 'https://i.imgur.com/j6sDEOt.png',
    },
    {
        'title': 'American soldier saving two Vietnamese children during the Vietnam War in 1968',
        'image': 'https://i.imgur.com/KutBakT.png',
    },
    {
        'title': 'Red Cross nurse jotting down the last words of a soldier on his deathbed in 1917',
        'image': 'https://i.imgur.com/Y7ziMVO.png',
    },
]


@bot.message_handler(commands=['historicalphotos'])
def historical_photos(message):
    try:
        historical = random.choice(historicals)

        bot.send_photo(
            message.chat.id,
            historical['image'],
            caption=f"<b>{historical['title']}</b>",
            parse_mode='HTML',
            reply_to_message_id=message.message_id,
        )
    except Exception as e:
        logger.info('-' * 50)
        logger.error(f'Error sending historical image: {e}')
        logger.info('-' * 50)
