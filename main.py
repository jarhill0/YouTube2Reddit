from functions import log_in_to_reddit
from functions import get_subbed
from functions import find_epoch
from functions import get_videos
from functions import write_last_run


with open('config/last_run.txt') as f:
    last_run = int(f.read().strip())
videos_to_submit = []
subbed_users = set()
subbed_channels = set()
with open('config/target_sub.txt') as f:
    target_sub = f.read().strip()

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
    try:
        reddit.subreddit(target_sub).submit('%s — %s' % (video['title'], video['author']),
                                            url=video['url'],
                                            resubmit=False,
                                            send_replies=False)
    except:
        print('Already submitted.')
write_last_run()
