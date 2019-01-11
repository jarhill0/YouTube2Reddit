import praw

import config
from memory import VideoMemoryParent


class YouTube2Reddit:
    def __init__(self):
        self.reddit = praw.Reddit('YouTube2Reddit', user_agent='YouTube2Reddit')
        self.subreddit = self.reddit.subreddit(config.sub_name)
        self.memory = VideoMemoryParent(self.subreddit)

    def first_run(self):
        self.memory.already_submitted.add_all(video['id'] for video in self.memory.new_videos())

    def main(self):
        submitted_this_run = set()

        for video in self.memory.new_videos():
            try:
                self.subreddit.submit('{} — {}'.format(video['title'], video['author']),
                                      url=video['url'],
                                      resubmit=False,
                                      send_replies=False)
            except praw.exceptions.APIException:
                print('Already submitted {!r} by {!r}.'.format(video['title'], video['author']))
            finally:
                # Either way, it's already submitted.
                submitted_this_run.add(video['id'])

        self.memory.already_submitted.add_all(submitted_this_run)


if __name__ == '__main__':
    YouTube2Reddit().main()
