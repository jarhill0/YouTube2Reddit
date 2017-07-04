import first_run
import functions


def is_username():
    while True:
        user_or_channel = input('User or channel? [u/c]\n').lower()
        if user_or_channel in ['u', 'user']:
            return True
        elif user_or_channel in ['c', 'channel']:
            return False
        else:
            print(
                'Invalid. Enter U for user or C for channel (channel looks like UC2C_jShtL725hvbm1arSV9w; '
                'user looks like cgpgrey).')


def new_subscription():
    new_sub = input('Enter channel ID or username.\n')
    return new_sub.strip()


def subscribe():
    new_users = []
    new_channels = []

    while True:
        if is_username():
            new_users.append(new_subscription())
        else:
            new_channels.append(new_subscription())

        if input('Add another subscription? [y/n]\n').lower() not in ['yes', 'y']:
            break

    reddit = functions.log_in_to_reddit()
    functions.extend_subbed_users(reddit, new_users)
    functions.extend_subbed_channels(reddit, new_channels)
    first_run.list_old_videos(new_users, new_channels)


if __name__ == '__main__':
    print('Subscribe YouTube2Reddit to another channel.')
    subscribe()
