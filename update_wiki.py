from functions import log_in_to_reddit
from functions import get_subbed_users
from functions import get_subbed_channels


def update_wiki():
    subbed_users = get_subbed_users()
    subbed_channels = get_subbed_channels()
    reddit = log_in_to_reddit()
    with open('config/target_sub.txt') as f:
        target_sub = f.read().strip()

    subbed_users_wiki = ''
    for user in subbed_users:
        subbed_users_wiki += user + '  \n'
    subbed_channels_wiki = ''
    for channel in subbed_channels:
        subbed_channels_wiki += channel + '  \n'

    reddit.subreddit(target_sub).wiki.create('subbed_users', subbed_users_wiki)
    reddit.subreddit(target_sub).wiki.create('subbed_channels', subbed_channels_wiki)
