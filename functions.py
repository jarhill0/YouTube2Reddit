import datetime
import time

import config
import feedparser
import praw


def log_in_to_reddit():
    return praw.Reddit(
        'YouTube2Reddit',
        user_agent='YouTube2Reddit')


def get_subbed_users(reddit):
    return set(read_wiki_subscriptions(reddit, config.sub_name, 'subbed_users'))


def get_subbed_channels():
    return set(read_wiki_subscriptions(reddit, config.sub_name, 'subbed_channels'))


def get_videos(channel_feed):
    time.sleep(.75)
    feed = feedparser.parse(channel_feed)
    items = []
    for post in reversed(feed.entries):
        items.append({
            'title': post.title,
            'author': post.author,
            'url': post.link
        })
    return items


def read_wiki_subscriptions(reddit, subreddit_name, page):
    return [x for x in reddit.subreddit(subreddit_name).wiki[page].content_md.split() if x != '']
