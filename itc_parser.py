# author = "garry"

from lxml import html
from dateutil import parser

from bot_config import TAGS


def get_all_articles_from_page(html_doc) -> list:
    root = html.fromstring(html_doc)
    news_div = root.xpath('//div[@class="col-xs-8 col-txt"]')
    result = []
    try:
        for element in news_div:
            news = {}
            h = element.xpath('h2/a')[0]
            article_date = element.xpath('div[@class="entry-header"]/div/span/time[@class="published"]')[0].items()
            dt = parser.parse(article_date[1][1])
            body = element.xpath('div[@class="entry-excerpt hidden-xs"]')[0].text.strip()

            news["date"] = int(dt.timestamp())
            news["url"] = h.items()[0][1]
            news["head"] = h.text
            news["body"] = body
            news["tags"] = find_tag(f"{h.text} {body}")
            result.append(news)
    except:
        pass
    return result


def find_tag(text):
    return [tag for tag in TAGS if tag in text.lower()]

