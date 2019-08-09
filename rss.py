import feedparser
import numpy
import pandas as pd

def News():
    NewsFeed = feedparser.parse("https://www.investing.com/rss/news_301.rss")
    NewsFeed2 = feedparser.parse("https://www.investing.com/rss/302.rss")
    entry = []
    entry2 = []
    x = 0
    while x < 10:
        entry.append(NewsFeed.entries[x].title + " : " + NewsFeed.entries[x].published + " : " + NewsFeed.entries[x].link)
        entry2.append(NewsFeed2.entries[x].title + " : " + NewsFeed2.entries[x].published + " : " + NewsFeed2.entries[x].link)
        x = x + 1
    Data = {
        "NEWS":entry,
        "Analysis":entry2
    }
    df = pd.DataFrame(Data)
    return df
#News()