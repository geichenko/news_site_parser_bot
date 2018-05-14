from collections import namedtuple
from telegram import InlineKeyboardButton

site_url = "http://itc.ua/"
mongodb_host = "clustertest-x6pax.mongodb.net/test"
bd_credentials = ("geich", "geich_test_rereirf")
bd_name = "itc"
bd_collection_name = "articles"
TAGS = ['iphone', 'ios', 'macos', 'osx', 'android', 'blackberry', 'oneplus', 'samsung', 'lg', 'google', 'pixel',
        'meizu', 'oppo', 'htc', 'xiaomi', 'huawei', 'honor', 'mac', 'macbook', 'windows', 'linux', 'ubuntu', 'dell',
        'hp', 'asus', 'debian', 'red hat']
bot_token = "585515459:AAEMzff5y6pl5XoNNbEG_Xp3cZcwXWj9qnU"

buttons_name = namedtuple("buttons_name",
                          ["to_start", "to_tags", "to_date", "to_today", "search_by_tags", "search_by_date",
                           "search_by_today", "no_result", "view_more", "show_today", "show_yesterday",
                           "show_custom_date"])

inline_buttons = buttons_name(
    InlineKeyboardButton("Go back to Main List", callback_data="go to start"),
    InlineKeyboardButton("Go back to Tags List", callback_data="go to tags"),
    InlineKeyboardButton("Go to Date Search List", callback_data="go to date"),
    InlineKeyboardButton("Go back to Today List", callback_data="go to today"),
    InlineKeyboardButton("Search By Tags", callback_data="go to tags"),
    InlineKeyboardButton("Search By Date", callback_data="go to date"),
    InlineKeyboardButton("All Topics By Today", callback_data="go to today"),
    InlineKeyboardButton("There are no any result", callback_data="empty"),
    InlineKeyboardButton("View More", callback_data="view more"),
    InlineKeyboardButton("View Today Topics", callback_data="go to today"),
    InlineKeyboardButton("View Yesterday Topics", callback_data="go to yesterday"),
    InlineKeyboardButton("View Topics For A Custom Date", callback_data="go to custom date"),
)