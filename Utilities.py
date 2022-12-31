from rss_parser import Parser
import Summarize
from requests import get

# import requests
# from bs4 import BeautifulSoup


def get_summary(summary):
    return Summarize.summarize(summary, 0.3)


def get_rss_news_data(link):
    print(link)
    titles = []
    try:
        xml = get(link)

        parser = Parser(xml=xml.content)

        feed = parser.parse()

        num = 0
        titles.append(feed.title)
        for i in feed.feed:
            title = i.title.replace("\"", "")
            title = title.replace("\'", "")
            str_title = title.encode("ascii", "ignore")
            str_1title = str_title.decode()

            # summary = i.description.replace("\"", "")
            # summary = summary.replace("\'", "")
            # str_summary = summary.encode("ascii", "ignore")
            # str_1summary = str_summary.decode()
            title_tokens = str_1title.split()
            str_1title = ''
            num_count = 0
            for j in title_tokens:
                str_1title += ' ' + j
                if num_count == 19 and len(title_tokens) > 20:
                    str_1title += '...'
                    print("sdfs")
                    break
                num_count += 1

            print(str_1title)
            date = i.publish_date.replace("\"", "")
            date = date.replace("\'", "")
            str_date = date.encode("ascii", "ignore")
            str_1date = str_date.decode()
            date_tokens = str_1date.split(' ', 4)
            str_1date = ' '
            if len(date_tokens) >= 4:
                for i in range(4):
                    str_1date += ' ' + date_tokens[i]
            print(link, str_1date, len(feed.feed))
            # if "description" in i and "published" in i and "title" in i:
            titles.append(
                [str_1title, str_1date])
            num += 1
            if(num > 15 or len(feed.feed) < num):
                break
        return titles
    except Exception as e:
        print(e)
    return titles
