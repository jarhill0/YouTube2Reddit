import praw
import feedparser
from time import mktime, struct_time, time
from datetime import datetime


def log_in_to_reddit():
    return praw.Reddit(
        'YouTube2Reddit',
        user_agent='YouTube2Reddit')


def get_subbed_users():
    subbed_users = set()
    with open('config/subbed_users.txt') as f:
        for creator in f.readlines():
            subbed_users.add(creator.strip())
    return subbed_users


def get_subbed_channels():
    subbed_channels = set()
    with open('config/subbed_channels.txt') as f:
        for creator in f.readlines():
            subbed_channels.add(creator.strip())
    return subbed_channels


def get_videos(channel_feed):
    feed = feedparser.parse(channel_feed)
    items = []
    for post in reversed(feed.entries):
        items.append({
            'title': post.title,
            'author': post.author,
            'url': post.link
        })
    return items


def write_last_run():
    with open('config/last_run.txt', 'w+') as f:
        f.write(str(int(time())))
