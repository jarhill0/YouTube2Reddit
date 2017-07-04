import functions


def update_wiki():
    subbed_users = list(functions.get_subbed_users())
    subbed_channels = list(functions.get_subbed_channels())
    reddit = functions.log_in_to_reddit()
    with open('config/target_sub.txt') as f:
        target_sub = f.read().strip()

    subbed_users_wiki = ''
    for user in sorted(subbed_users):  # sort is practically essential for readability
        subbed_users_wiki += user + '  \n'
    subbed_channels_wiki = ''
    for channel in sorted(subbed_channels):  # not necessary to sort; but it makes it nice to spot changes
        subbed_channels_wiki += channel + '  \n'

    reddit.subreddit(target_sub).wiki.create('subbed_users', subbed_users_wiki)
    reddit.subreddit(target_sub).wiki.create('subbed_channels', subbed_channels_wiki)


if __name__ == '__main__':
    update_wiki()
