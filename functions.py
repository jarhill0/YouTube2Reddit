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
    return set(read_wiki_subscriptions(reddit, config.sub_name, config.subbed_users_page_name))


def get_subbed_channels(reddit):
    return set(read_wiki_subscriptions(reddit, config.sub_name, config.subbed_channels_page_name))


def get_already_submitted(reddit):
    return set(read_wiki_subscriptions(reddit, config.sub_name, config.already_submitted_page_name))


def write_already_submitted(reddit, ids):
    if type(ids) not in [list, set]:
        raise ValueError("Expecting a list or set, not %s." % type(ids))
    preexisting_conditions = set(get_already_submitted(reddit))
    ids.update(preexisting_conditions)

    write_to_wiki(reddit, config.sub_name, config.already_submitted_page_name, ' '.join(ids))


def get_videos(channel_feed):
    time.sleep(.75)
    feed = feedparser.parse(channel_feed)
    items = []
    for post in reversed(feed.entries):
        items.append({
            'title': post.title,
            'author': post.author,
            'url': post.link,
            'id': post.yt_videoid
        })
    return items


def read_wiki_subscriptions(reddit, subreddit_name, page):
    return [x for x in reddit.subreddit(subreddit_name).wiki[page].content_md.split() if x != '']


def write_to_wiki(reddit, subreddit_name, page, content):
    reddit.subreddit(subreddit_name).wiki.create(page, content)
