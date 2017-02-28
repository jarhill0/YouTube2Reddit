from functions import log_in_to_reddit
from functions import get_subbed_users
from functions import get_subbed_channels
from functions import get_videos

run_it = input('WARNING! Running this script means that the bot will not post any videos to Reddit that were'
               ' posted prior to running this script. This is a good thing if you have never run the bot before,'
               ' as it will prevent spam, but it is probably a bad thing if you have run the bot before. Do you'
               ' wish to continue? [y/n] ').lower()
if run_it not in ['y', 'yes']:
    print('Exiting.')
    exit()

videos_to_submit = []
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

for video in videos_to_submit:
    submitted_this_run.append(video['url'])

with open('config/already_submitted.txt', 'w') as f:
    for url in submitted_this_run:
        f.write(url + '\n')
