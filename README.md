## Telegram bot for re-posting parsed content from some news site
A simple Python Telegram bot that parsed some news site and make this content be available from telegram bot. 
Interface inside this bot is build on buttons (InlineKeyboardButton)
Tested on Heroku.

### Used:
 - MongoDB for storing parsed content
 - Heroku
 - lxml for parsing html
 
##### All environment's vars are stored in the Heroku config

## Required
* Python 3.6
* [python-telegram-bot](https://github.com/leandrotoledo/python-telegram-bot) module (tested with version 2.5)
* [Flask](http://flask.pocoo.org/) microframework (tested with version 0.10.1)
* [lxml](http://lxml.de/) library for processing XML and HTML 
* [pymongo](https://api.mongodb.com/python/current/) distribution containing tools for working with MongoDB

## How to use
* Clone this repository
* Edit TELEGRAM TOKEN, URL, DB_CREDENTIAL in bot_config.py for local usage
* Start news_bot.py
* Start chatting in Telegram and enjoy your echoes! :)