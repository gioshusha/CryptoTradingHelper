import feedparser
import numpy
import pandas as pd

def News():
    NewsFeed = feedparser.parse("https://cointelegraph.com/rss/tag/ethereum")
    NewsFeed2 = feedparser.parse("https://cointelegraph.com/rss/tag/regulation")
    entry = []
    for news in NewsFeed.entries:
        newses = " " + news.title + " : " + news.published + " : " + news.link
        entry.append(newses)
    entry2 = []
    for news in NewsFeed2.entries:
        newses = " " + news.title + " : " + news.published + " : " + news.link
        entry2.append(newses)
    hp1 = []
    hp2 = []
    x = 0
    while x < 10:
        hp1.append(entry[x])
        hp2.append(entry2[x])
        x = x + 1
    Data = {
        "NEWS":entry,
        "Regulations":entry2
    }
    df = pd.DataFrame(Data)
    return df