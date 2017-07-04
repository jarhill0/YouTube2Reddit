import config
import functions
import praw

if __name__ == '__main__':
    videos_to_submit = []
    submitted_this_run = []
    target_sub = config.sub_name
    reddit = functions.log_in_to_reddit()

    with open('config/already_submitted.txt') as f:
        already_submitted = set(f.read().split('\n'))
        already_submitted.remove('')

    subbed_users = functions.get_subbed_users(reddit)
    subbed_channels = functions.get_subbed_channels(reddit)

    for user in subbed_users:
        videos = functions.get_videos('https://www.youtube.com/feeds/videos.xml?user=' + user)
        for video in videos:
            if video['id'] not in already_submitted:
                videos_to_submit.append(video)

    for channel_id in subbed_channels:
        videos = functions.get_videos('https://www.youtube.com/feeds/videos.xml?channel_id=' + channel_id)
        for video in videos:
            if video['id'] not in already_submitted:
                videos_to_submit.append(video)

    for video in videos_to_submit:
        try:
            reddit.subreddit(target_sub).submit('%s — %s' % (video['title'], video['author']),
                                                url=video['url'],
                                                resubmit=False,
                                                send_replies=False)
        except praw.exceptions.APIException:
            print('Already submitted %s by %s.' % (video['title'], video['author']))
        else:
            submitted_this_run.append(video['id'])

    functions.write_already_submitted(reddit, submitted_this_run)
