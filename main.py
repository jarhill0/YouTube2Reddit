import praw

import config
from memory import VideoMemoryParent


class YouTube2Reddit:
    def __init__(self):
        self.reddit = praw.Reddit("YouTube2Reddit", user_agent="YouTube2Reddit")
        self.subreddit = self.reddit.subreddit(config.sub_name)
        self.memory = VideoMemoryParent(self.subreddit)

    def check_inbox(self):
        for message in self.reddit.inbox.unread(mark_read=True):
            message.mark_read()

            if hasattr(message, "subject") and "subscribe" in message.subject.lower():
                subject = message.subject.lower()
                if ("users" in subject) == ("channels" in subject):
                    message.reply(
                        "Please use exactly one of `users` or `channels` in your subject line."
                    )
                    continue

                creators = message.body.strip().split()
                if "users" in subject:
                    self.memory.add_subscriptions(users=creators)
                else:  # 'channels' in subject
                    self.memory.add_subscriptions(channels=creators)

                message.reply(
                    "The following {creators} have been added:\n\n{lst}".format(
                        creators="users" if "users" in subject else "channels",
                        lst="\n".join("    " + creator for creator in creators),
                    )
                )

    def first_run(self):
        self.memory.already_submitted.add_all(
            video["id"] for video in self.memory.new_videos()
        )

    def main(self):
        submitted_this_run = set()

        for video in self.memory.new_videos():
            try:
                self.subreddit.submit(
                    "{} — {}".format(video["title"], video["author"]),
                    url=video["url"],
                    resubmit=False,
                    send_replies=False,
                )
            except praw.exceptions.APIException:
                print(
                    "Already submitted {!r} by {!r}.".format(
                        video["title"], video["author"]
                    )
                )
            finally:
                # Either way, it's already submitted.
                submitted_this_run.add(video["id"])

        self.memory.already_submitted.add_all(submitted_this_run)


if __name__ == "__main__":
    yt2r = YouTube2Reddit()
    yt2r.check_inbox()
    yt2r.main()
