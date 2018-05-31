#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, time, random, requests
from datetime import datetime
from bson.objectid import ObjectId
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from mdb import MDB
import bot_config, site_parser


class NewsBot(object):
    def __init__(self):
        self.__message_id = [int(), str()]
        self.__db = MDB(*bot_config.bd_credentials, bot_config.bd_name, bot_config.bd_collection_name)
        self.parsing_resource = bot_config.site_url
        self.__tags = bot_config.TAGS
        self.__bot_token = bot_config.bot_token
        self.__buttons = bot_config.inline_buttons
        self.__time_start = int()
        self.view_more_data = []

    def start(self, bot, update):
        if int(time.time()) > self.__time_start + 600:
            self.update_db()
            self.__time_start = int(time.time())
        update.message.reply_text("Hi, this is news bot, \nChose your option:", reply_markup=self.make_start_view())

    def callback_actions(self, bot, update):
        query = update.callback_query
        print("message_id ", query.message.message_id)
        print("data ", f"-{query.data}-")

        if self.__message_id[0] == query.message.message_id and self.__message_id[1] == query.data:
            return None
        self.__message_id = query.message.message_id, query.data
        if query.data == "go to tags":
            self.show_tags_view(query)
        if query.data == "go to start":
            self.show_start_view(query)
        if query.data == "go to date":
            self.show_date_view(query)
        if query.data in self.__tags:
            self.show_entries_by_tag(query)
        if query.data == "go to today":
            self.show_day_entries(query)
        if query.data == "go to yesterday":
            yesterday = datetime.fromtimestamp(int(time.time())-86400).strftime('%Y-%m-%d')
            self.show_day_entries(query, yesterday)
        if query.data == "go to custom date":
            self.show_custom_date_view(query)
        if "view more" in query.data:
            self.show_more_entries(query)
        if "article_id" in query.data:
            _id = query.data.split("_")[2]
            self.show_article(query, _id)
        else:
            print("-empty-")

    def show_tags_view(self, query):
        markup = InlineKeyboardMarkup(self.make_columns(
            list(map(lambda x: InlineKeyboardButton(x, callback_data=x), self.__tags)), 4))
        query.edit_message_text('Please choose tag:', reply_markup=markup)

    def make_start_view(self):
        if int(time.time()) > self.__time_start + 600:
            self.update_db()
            self.__time_start = int(time.time())
        markup = InlineKeyboardMarkup([[
            self.__buttons.search_by_date,
            self.__buttons.search_by_tags,
            self.__buttons.search_by_today
        ]])
        return markup

    def show_start_view(self, query):
        query.edit_message_text('Please choose option:', reply_markup=self.make_start_view())

    def show_date_view(self, query):
        markup = InlineKeyboardMarkup([
            [self.__buttons.show_today, self.__buttons.show_yesterday],
            [self.__buttons.show_custom_date]
        ])
        query.edit_message_text('Please choose option:', reply_markup=markup)

    def show_custom_date_view(self, query):
        query.edit_message_text('Please enter specific date in format YYYY-MM-DD:')

    def show_day_entries(self, query, day: str = None):
        query.edit_message_text('Today results:', reply_markup=InlineKeyboardMarkup(self.make_day_entries(day)))

    def make_day_entries(self, day: str = None):
        day = day or time.strftime("%Y-%m-%d")
        db_search_result = self.__db.get_entries_by_date(day)
        if db_search_result.count():
            res = self.__make_buttons_for_view(db_search_result)
            print(res)
            return res
        else:
            print([self.__buttons.no_result])
            return [[self.__buttons.no_result], self.make_back_footer()]

    def show_entries_by_tag(self, query):
        db_search_result = self.__db.get_entries_by_tag(query.data)
        all_tags = self.__make_buttons_for_view(db_search_result, self.__buttons.to_tags)
        query.edit_message_text(f'Results by tag {query.data}:', reply_markup=InlineKeyboardMarkup(all_tags))

    def show_more_entries(self, query):
        try:
            entries = next(self.view_more_data)
            view_more_btn = InlineKeyboardButton("View More", callback_data=f"view more {random.randint(1,100)}")
            if len(entries) < 10:
                entries.append(self.make_back_footer())
            else:
                entries.append(self.make_back_footer(view_more_btn))
        except:
            entries = self.make_back_footer(self.__buttons.to_tags)
        query.edit_message_text(f'Results:', reply_markup=InlineKeyboardMarkup(entries))

    def custom_date_handler(self, bot, update):
        message_text = update.message.text
        re_parsing = re.findall(r'\d\d\d\d-\d\d-\d\d', message_text)
        if re_parsing:
            date = re_parsing[0]
            print(date)
            print(dir(update.message))
            update.message.reply_text(f"Topics for the {date}",
                                      reply_markup=InlineKeyboardMarkup(self.make_day_entries(date)))
        else:
            pass

    def show_article(self, query, article_id: str):
        db_search_result = self.__db.collection.find_one({"_id":ObjectId(article_id)})
        print(db_search_result)
        if db_search_result:
            entry = db_search_result
            url, head, body = entry.get("url"), entry.get("head"), entry.get("body")
            link_to_page = InlineKeyboardButton("go to full view", url=url)
            buttons = [[link_to_page], self.make_back_footer(self.__buttons.to_tags)]
            query.edit_message_text(text=f'<b>{head}</b>\n{body}',
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=InlineKeyboardMarkup(buttons))

    def __make_buttons_for_view(self, db_search_result, *footer_btns):
        all_entries = []
        if db_search_result.count():
            for result in db_search_result:
                print(result)
                all_entries.append([InlineKeyboardButton(result.get("head"), callback_data=f"article_id_{result.get('_id')}")])
        else:
            all_entries.append([self.__buttons.no_result])
        if len(all_entries) > 10:
            resp = all_entries[:10]
            self.view_more_data = self.get_data_for_view_more(all_entries[10:])
            resp.append(self.make_back_footer(*footer_btns, self.__buttons.view_more))
            return resp
        else:
            all_entries.append(self.make_back_footer(*footer_btns))
            return all_entries

    def get_data_for_view_more(self, bd_search_result: list() = None):
        all_data = []
        if bd_search_result:
            all_data = self.make_columns(bd_search_result, 10)
        for res in all_data:
            yield res

    def make_back_footer(self, *extra_buttons: InlineKeyboardButton):
        footer_btns = [self.__buttons.to_start]
        if extra_buttons:
            for button in extra_buttons:
                footer_btns.append(button)
        return footer_btns

    @staticmethod
    def make_columns(l: list, n: int):
        return [l[i:i + n] for i in range(0, len(l), n)]

    def update_db(self):
        time_start = int(time.time())
        time_end = self.__db.get_last_entries().get("date") + 30
        page = 1
        while time_start > time_end:
            url = f"{self.parsing_resource}page/{page}/"
            page += 1
            r = requests.get(url)
            r.encoding = 'utf-8'
            html_text = r.text
            all_articles_from_page = site_parser.get_all_articles_from_page(html_text)
            for article in all_articles_from_page:
                time_start = article.get("date")
                if time_start > time_end:
                    print(article.get("head"))
                    self.__db.write(article)

    def run(self):
        updater = Updater(self.__bot_token)
        updater.dispatcher.add_handler(CommandHandler('start', self.start))
        updater.dispatcher.add_handler(CallbackQueryHandler(self.callback_actions))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, self.custom_date_handler))
        updater.start_polling()
        updater.idle()


news_bot = NewsBot()
news_bot.run()
