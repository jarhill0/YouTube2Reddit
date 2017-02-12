import feedparser
from time import mktime
from time import struct_time
from time import time
from datetime import datetime
import praw

with open('config/last_run.txt') as f:
    last_run = int(f.read().strip())
videos_to_submit = []
subbed_users = set()
subbed_channels = set()
with open('config/target_sub.txt') as f:
    target_sub = f.read().strip()


def get_subbed():
    global subbed_users
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


def read_login_resource(name):
    with open('login/%s.txt' % name) as f:
        return f.read().strip()


def log_in_to_reddit():
    global reddit
    client_id = read_login_resource('client_id')
    client_secret = read_login_resource('client_secret')
    username = read_login_resource('username')
    password = read_login_resource('password')
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent='YouTube2Reddit',
        username=username,
        password=password)


def write_last_run():
    with open('config/last_run.txt', 'w+') as f:
        f.write(str(int(time())))


get_subbed()

for user in subbed_users:
    videos = get_videos('https://www.youtube.com/feeds/videos.xml?user=' + user)
    for video in videos:
        videos_to_submit.append(video)

for channel_id in subbed_channels:
    videos = get_videos('https://www.youtube.com/feeds/videos.xml?channel_id=' + channel_id)
    for video in videos:
        videos_to_submit.append(video)

log_in_to_reddit()

for video in videos_to_submit:
    reddit.subreddit(target_sub).submit('%s — %s' % (video['title'], video['author']),
                                        url=video['url'],
                                        resubmit=False,
                                        send_replies=False)
write_last_run()
