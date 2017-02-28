from functions import log_in_to_reddit
from functions import get_subbed_users
from functions import get_subbed_channels
from functions import find_epoch
from functions import get_videos
from functions import write_last_run

videos_to_submit = []

with open('config/target_sub.txt') as f:
    target_sub = f.read().strip()

subbed_users = get_subbed_users()
subbed_channels = get_subbed_channels()

for user in subbed_users:
    videos = get_videos('https://www.youtube.com/feeds/videos.xml?user=' + user)
    for video in videos:
        videos_to_submit.append(video)

for channel_id in subbed_channels:
    videos = get_videos('https://www.youtube.com/feeds/videos.xml?channel_id=' + channel_id)
    for video in videos:
        videos_to_submit.append(video)

reddit = log_in_to_reddit()

for video in videos_to_submit:
    try:
        reddit.subreddit(target_sub).submit('%s — %s' % (video['title'], video['author']),
                                            url=video['url'],
                                            resubmit=False,
                                            send_replies=False)
    except praw.exceptions.APIException:
        print('Already submitted.')
write_last_run()
