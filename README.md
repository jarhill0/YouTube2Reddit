# YouTube2Reddit: a Python script to periodically post YouTube videos from specific channels to a specific subreddit

This script is designed to be called periodically in its home directory. Its purpose is to post new YouTube videos from predefined YouTube channels to a predefined subreddit.

Since it's designed to be called periodically, I recommend running it on a cronjob at least once a day.

**Setup (may be incomplete)**:

1. Run `pip install praw` and `pip install feedparser` on your system (note: you may have to replace `pip` with `pip3` in those commands, as I had to).
2. Create an OAuth2 app as described [here](https://github.com/reddit/reddit/wiki/OAuth2). Make sure you are signed into the account you plan to run this script from. Note the client ID and the client secret.
3. Open the `config` folder and create the following text files:
    - `last_run.txt`: Epoch time (seconds since January 1, 1970). I recommend you populate it with [the current epoch time](http://www.epochconverter.com/clock). The file only needs to be initialized once, and afterwards it will be automatically updated upon successful completion of the script. The file is used to make sure that the bot only posts videos that are new since the time it last ran.
    - `subbed_users.txt`: A list of Youtube usernames you wish to be "subscribed" to, one per line. **Note: These are usernames (like `CGPGrey`), not channel names (like `UCekQr9znsk2vWxBo3YiLq2w`).**
    - `subbed_channels.txt`: A list of Youtube channel names you wish to be "subscribed" to, one per line. Do not duplicate channels from `subbed_users.txt`. Both files exist because some channels do not have usernames, only cryptic channel names. **Note: These are channel names (like `UCekQr9znsk2vWxBo3YiLq2w`), not usernames (like `CGPGrey`).**
    - `target_sub.txt`: The name of the subreddit the script should submit to. I recommend that the account you run the script on should be an approved submitted or a moderator in whatever subreddit it submits to, because it will often submit several posts at once, which would be seen as spam in a subreddit where the account is not an approved submitter or a moderator.
4. Create `praw.ini` in the following format:
    ```
    
    [YouTube2Reddit]
    client_id=
    client_secret=
    username=
    password=
    
    ```
    Define each variable immediately after the = sign in the following way:
    - `client_id.txt`: The client ID from step 2.
    - `client_secret.txt`: The client secret from step 2.
    - `username.txt`: The username you want this script to run on. Make sure it has enough karma to post without captchas.
    - `password.txt`: The password for that account
5. Set up a cronjob (or other method of calling this script) that calls `main.py` at least daily, or as often as you want. **Make sure to run the script in the same directory it is in!** The command I will use in my cronjob is `cd ~/YouTube2Reddit && python3 main.py`.
