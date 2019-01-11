from main import YouTube2Reddit


def main():
    run_it = input(
        'WARNING! Running this script means that the bot will not post any videos to Reddit that were'
        ' posted prior to running this script. This is a good thing if you have never run the bot before,'
        ' as it will prevent spam, but it is probably a bad thing if you have run the bot before. Do you'
        ' wish to continue? [y/n] ').lower() in ['y', 'yes']
    if not run_it:
        print('Exiting.')
    else:
        YouTube2Reddit().first_run()


if __name__ == '__main__':
    main()
