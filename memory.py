import time

import feedparser
from prawcore.exceptions import NotFound

import config


class VideoMemoryParent:
    def __init__(self, subreddit):
        self.subbed_users = VideoMemory(subreddit, config.subbed_users_page_name, delimiter='  \n')
        self.subbed_channels = VideoMemory(subreddit, config.subbed_channels_page_name, delimiter='  \n')
        self.already_submitted = VideoMemory(subreddit, config.already_submitted_page_name)

    def _new_videos_from_creator(self, creator_name):
        assert (creator_name in self.subbed_users) != (creator_name in self.subbed_channels)
        base_url = config.channel_base_url if creator_name in self.subbed_channels else config.user_base_url
        yield from self._videos(base_url + creator_name)

    def _videos(self, channel_feed):
        if config.self_rate_limit:
            time.sleep(1)
        feed = feedparser.parse(channel_feed)

        for post in reversed(feed.entries):
            if post.yt_videoid not in self.already_submitted:
                yield {
                    'title': post.title,
                    'author': post.author,
                    'url': post.link,
                    'id': post.yt_videoid
                }

    def add_subscriptions(self, channels=None, users=None):
        new_videos = set()
        if channels is not None:
            self.subbed_channels.add_all(channels)
            new_videos.update(video['id'] for channel in channels for video in self._new_videos_from_creator(channel))
        if users is not None:
            self.subbed_users.add_all(users)
            new_videos.update(video['id'] for user in users for video in self._new_videos_from_creator(user))
        self.already_submitted.add_all(new_videos)

    def new_videos(self):
        for user in self.subbed_users:
            yield from self._new_videos_from_creator(user)
        for channel_id in self.subbed_channels:
            yield from self._new_videos_from_creator(channel_id)


class VideoMemory:
    def __contains__(self, item):
        self._load()
        return item in self._contents

    def __init__(self, subreddit, wiki_path, delimiter=' '):
        self.subreddit = subreddit
        self.wiki_path = wiki_path
        self._contents = None
        self.delimiter = delimiter

    def __iter__(self):
        self._load()
        return iter(self._contents)

    def _load(self):
        if self._contents is None:
            try:
                self._contents = set(
                    x for x in self.subreddit.wiki[self.wiki_path].content_md.split() if x != '')
            except NotFound:
                self._contents = set()

    def _dump(self):
        print('Updating wiki page {}…'.format(self.wiki_path))
        self.subreddit.wiki.create(self.wiki_path, self.delimiter.join(sorted(self._contents)))

    def add_all(self, items):
        if any(item not in self for item in items):
            self._contents.update(items)
            self._dump()
