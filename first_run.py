import functions
import config


def list_old_videos(subbed_users, subbed_channels):
    videos_to_submit = []

    for user in subbed_users:
        videos_to_submit.extend(functions.get_videos(config.user_base_url + user))
    for channel_id in subbed_channels:
        videos_to_submit.extend(functions.get_videos(config.channel_base_url + channel_id))

    submitted_this_run = [video['id'] for video in videos_to_submit]
    functions.write_already_submitted(functions.log_in_to_reddit(), submitted_this_run)


def main():
    run_it = input(
        'WARNING! Running this script means that the bot will not post any videos to Reddit that were'
        ' posted prior to running this script. This is a good thing if you have never run the bot before,'
        ' as it will prevent spam, but it is probably a bad thing if you have run the bot before. Do you'
        ' wish to continue? [y/n] ').lower() in ['y', 'yes']
    if not run_it:
        print('Exiting.')
    else:
        list_old_videos(functions.get_subbed_users(), functions.get_subbed_channels())


if __name__ == '__main__':
    main()
