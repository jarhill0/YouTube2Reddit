import functions
import praw

if __name__ == '__main__':
    videos_to_submit = []

    with open('config/target_sub.txt') as f:
        target_sub = f.read().strip()
    with open('config/already_submitted.txt') as f:
        already_submitted = set(f.read().split('\n'))
        already_submitted.remove('')
    submitted_this_run = []

    subbed_users = functions.get_subbed_users()
    subbed_channels = functions.get_subbed_channels()

    for user in subbed_users:
        videos = functions.get_videos('https://www.youtube.com/feeds/videos.xml?user=' + user)
        for video in videos:
            if video['url'] not in already_submitted:
                videos_to_submit.append(video)

    for channel_id in subbed_channels:
        videos = functions.get_videos('https://www.youtube.com/feeds/videos.xml?channel_id=' + channel_id)
        for video in videos:
            if video['url'] not in already_submitted:
                videos_to_submit.append(video)

    reddit = functions.log_in_to_reddit()

    for video in videos_to_submit:
        try:
            reddit.subreddit(target_sub).submit('%s — %s' % (video['title'], video['author']),
                                                url=video['url'],
                                                resubmit=False,
                                                send_replies=False)
        except praw.exceptions.APIException:
            print('Already submitted %s by %s.' % (video['title'], video['author']))
        else:
            submitted_this_run.append(video['url'])

    with open('config/already_submitted.txt', 'a') as f:
        for url in submitted_this_run:
            f.write(url + '\n')
