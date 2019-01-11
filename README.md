# YouTube2Reddit: a Python script to periodically post YouTube videos from specific channels to a specific subreddit

This script is designed to be called periodically in its home directory. Its purpose is to post new YouTube videos from predefined YouTube channels to a predefined subreddit.

Since it's designed to be called periodically, I recommend running it on a cronjob at least once a day.

**Setup (may be incomplete)**:

1. Run `pip install praw` and `pip install feedparser` on your system (note: you may have to replace `pip` with `pip3` in those commands, as I had to).
2. Create an OAuth2 app as described [here](https://github.com/reddit/reddit/wiki/OAuth2). Make sure you are signed into the account you plan to run this script from. Note the client ID and the client secret.
3. Open the `config.py` file and edit the following variables:
    - `sub_name`: The name of the subreddit your bot is moderator of.
4. Create `praw.ini` in the following format:
    ```
    
    [YouTube2Reddit]
    client_id=
    client_secret=
    username=
    password=
    
    ```
    Define each variable immediately after the = sign in the following way:

    - `client_id`: The client ID from step 2.
    - `client_secret`: The client secret from step 2.
    - `username`: The username you want this script to run on. Make sure it has enough karma to post without captchas.
    - `password`: The password for that account  

    The `praw.ini` file can go either in the directory you plan to execute the script from (as CWD) or in ~/.config/ .
5. Set up a cronjob (or other method of calling this script) that calls `main.py` at least daily, or as often as you want. The command I use in my cronjob is `python3 ~/YouTube2Reddit/main.py`.
6. Run `first_run.py` with `python3 first_run.py`.
