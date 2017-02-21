import praw
import feedparser
from time import mktime
from time import struct_time
from time import time
from datetime import datetime

def log_in_to_reddit():
    global reddit
    reddit = praw.Reddit(
        'YouTube2Reddit',
        user_agent='YouTube2Reddit')


def get_subbed():
    global subbed_users
    global subbed_channels
    subbed_users = set()
    subbed_channels = set()
    with open('config/subbed_users.txt') as f:
        for creator in f.readlines():
            subbed_users.add(creator.strip())
    with open('config/subbed_channels.txt') as f:
        for creator in f.readlines():
            subbed_channels.add(creator.strip())


def find_epoch(datetime_object):
    epoch = datetime.utcfromtimestamp(0)
    return int((datetime.fromtimestamp(mktime(struct_time(datetime_object))) - epoch).total_seconds())


def get_videos(channel_feed):
    feed = feedparser.parse(channel_feed)
    items = []
    for post in reversed(feed.entries):
        if find_epoch(post.published_parsed) > last_run:
            items.append(dict([
                ('title', post.title),
                ('author', post.author),
                ('url', post.link)
            ]))
    return items


def write_last_run():
    with open('config/last_run.txt', 'w+') as f:
        f.write(str(int(time())))
