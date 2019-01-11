from main import YouTube2Reddit


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


def new_subscription(is_user=False):
    new_sub = input('Enter {}.\n'.format('username' if is_user else 'channel ID'))
    return new_sub.strip()


def subscribe():
    new_users = set()
    new_channels = set()

    while True:
        is_user = is_username()
        if is_user:
            new_users.add(new_subscription(is_user=is_user))
        else:
            new_channels.add(new_subscription(is_user=is_user))

        if input('Add another subscription? [y/n]\n').lower() not in ['yes', 'y']:
            break

    YouTube2Reddit().memory.add_subscriptions(channels=new_channels, users=new_users)


if __name__ == '__main__':
    print('Subscribe YouTube2Reddit to another channel.')
    subscribe()
