import time

import feedparser
import praw

import config


def log_in_to_reddit():
    return praw.Reddit('YouTube2Reddit', user_agent='YouTube2Reddit')


def get_subbed_users(reddit):
    return set(read_wiki_subscriptions(reddit, config.sub_name, config.subbed_users_page_name))


def get_subbed_channels(reddit):
    return set(read_wiki_subscriptions(reddit, config.sub_name, config.subbed_channels_page_name))


def get_already_submitted(reddit):
    return set(read_wiki_subscriptions(reddit, config.sub_name, config.already_submitted_page_name))


def extend_subbed_users(reddit, new_users):
    if new_users:
        subs = get_subbed_users(reddit)
        subs.update(new_users)
        write_to_wiki(reddit, config.subbed_users_page_name, '  \n'.join(sorted(subs)))


def extend_subbed_channels(reddit, new_channels):
    if new_channels:
        subs = get_subbed_channels(reddit)
        subs.update(new_channels)
        write_to_wiki(reddit, config.subbed_channels_page_name, '  \n'.join(sorted(subs)))


def write_already_submitted(reddit, ids):
    try:
        ids = set(ids)
    except TypeError:
        raise ValueError("Expecting a list or set or other iterable, not %s." % type(ids))
    if len(ids) > 0:
        preexisting_conditions = set(get_already_submitted(reddit))
        ids.update(preexisting_conditions)

        write_to_wiki(reddit, config.already_submitted_page_name, ' '.join(sorted(ids)))


def get_videos(channel_feed):
    if config.self_rate_limit:
        time.sleep(1)
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


def write_to_wiki(reddit, page, content):
    print('Updating wiki page %s…' % page)
    reddit.subreddit(config.sub_name).wiki.create(page, content)
