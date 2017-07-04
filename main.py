import config
import functions
import praw


def main():
    videos_to_submit = []
    submitted_this_run = {}
    target_sub = config.sub_name
    reddit = functions.log_in_to_reddit()
    already_submitted = functions.get_already_submitted(reddit)
    subbed_users = functions.get_subbed_users(reddit)
    subbed_channels = functions.get_subbed_channels(reddit)

    for user in subbed_users:
        videos = functions.get_videos('https://www.youtube.com/feeds/videos.xml?user=' + user)
        videos_to_submit.extend(v for v in videos if v['id'] not in already_submitted)

    for channel_id in subbed_channels:
        videos = functions.get_videos('https://www.youtube.com/feeds/videos.xml?channel_id=' + channel_id)
        videos_to_submit.extend(v for v in videos if v['id'] not in already_submitted)

    for video in videos_to_submit:
        try:
            reddit.subreddit(target_sub).submit('%s — %s' % (video['title'], video['author']),
                                                url=video['url'],
                                                resubmit=False,
                                                send_replies=False)
        except praw.exceptions.APIException:
            print('Already submitted %s by %s.' % (video['title'], video['author']))
        finally:
            # Either way, it's already submitted.
            submitted_this_run.add(video['id'])

    functions.write_already_submitted(reddit, submitted_this_run)


if __name__ == '__main__':
    main()
