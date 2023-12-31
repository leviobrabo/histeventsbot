﻿<img src="https://i.imgur.com/sEetOYK.jpeg" align="right" width="200" height="200"/>

# Historical facts

[![](https://img.shields.io/badge/Telegram-@fatoshistbot-blue)](https://t.me/HistoricalEvents_Bot)
[![](https://img.shields.io/badge/Suporte-@kylorensbot-1b2069)](https://t.me/kylorensbot)

[Historical Facts](https://t.me/HistoricalEvents_bot) is a bot for Telegram that aims to spread knowledge of history and also to bring knowledge in a "light" and "calm" way to the entire public.

## Functionalities

-   Sends historical events of the day
    -   Private chat
    -   Channel
    -   Groups
-   Sends historical phrases
-   Sends Holidays of the day
-   Send Born of the day
-   Sends dead of the day
-   Sends images of historical events
    -   Private chat
    -   Channel
    -   Groups
-   Send historical curiosities
-   Send commemorative dates

*   Send quiz with historical questions 🆕
    -Chat
    -   Channel
*   Sends Presidents of each country 🆕

[![](https://i.imgur.com/MzZuN3G.jpeg)](#)

### Prerequisites

You will need to have the following tools installed on your machine:

-   [Git](https://git-scm.com)
-   [Python](https://www.python.org/)
-   [MongoDB](https://cloud.mongodb.com/)
-   [WIKIMEDIA](https://api.wikimedia.org/wiki/Feed_API/Reference/On_this_day)

### 🤖 Deploy on Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### 🤖 Running the bot locally

```bash
# Clone this repository
$ git clone https://github.com/leviobrabo/fatoshisbot.git

# Access the project folder in terminal/cmd
$ cd factshisbot

# Install dependencies

# Using pip:
$ pip3 install -r requirements.txt

# change the conf name
$ cp sample.bot.conf bot.conf

# Environment variables

# Create a file with bot.conf with any text editor and put:
[HISTORICALEVENTS]
TOKEN=
HIST_LOG=
HIST_CHANNEL=
BOT_NAME=
BOT_USERNAME=
OWNER_ID=
HIST_CHANNEL_POST =

[DB]
MONGO_CON=

[LOG]
LOG_PATH = /path/to/log/file

# Run the application
$ python3 factohistoricos.py

```

## Ready, the bot will already be running
