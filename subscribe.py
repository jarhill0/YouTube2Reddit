from update_wiki import update_wiki
from first_run import list_old_videos


def is_username():
    user_or_channel = input('User or channel? [u/c]\n').lower()
    if user_or_channel in ['u', 'user']:
        return True
    elif user_or_channel in ['c', 'channel']:
        return False
    else:
        print(
            'Invalid. Enter U for user or C for channel (channel looks like UC2C_jShtL725hvbm1arSV9w; user looks like cgpgrey).')
        return is_username()


def new_subscription():
    new_sub = input('Enter channel ID or username.\n')
    return new_sub.strip()


def subscribe():
    if is_username():
        new_sub = new_subscription()
        with open('config/subbed_users.txt', 'a') as f:
            f.write(new_sub + '\n')
        list_old_videos([new_sub], [])
    else:
        new_sub = new_subscription()
        with open('config/subbed_channels.txt', 'a') as f:
            f.write(new_sub + '\n')
        list_old_videos([], [new_sub])

    if input('Add another subscription? [y/n]\n').lower() in ['yes', 'y']:
        subscribe()


if __name__ == '__main__':
    print('Subscribe YouTube2Reddit to another channel.')
    subscribe()
    print('Updating wiki…')
    update_wiki()
