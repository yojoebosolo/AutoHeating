Watch the tutorial:

https://youtu.be/ch-9DpZL6Vg

Required Python modules:

    tapo
    requests

"crontab -e" config, to schedule code every 30 mins:

        0,30 * * * * sleep 5; cd /home/yojoe/Code && set -a && . /home/yojoe/Code/secrets.env && set +a && /home/yojoe/Code/.venv/bin/python /home/yojoe/Code/main.py >> /home/yojoe/Code/cron.log 2>&1

Following code to be run from python venv on the raspberry pi server to load environment variables
    
    set -a; . /home/yojoe/Code/secrets.env; set +a

Sometimes the environment variables get stuck (after making changes to secrets.env) and need to be refreshed:
1. Clear any stale vars in your current shell

        unset TAPO_USERNAME TAPO_PASSWORD TAPO_IP POSTCODE

2. Ensure the file is clean (LF only), then re-source it

        cd /home/yojoe/Code
        dos2unix secrets.env          # harmless if already LF

        set -a; . ./secrets.env; set +a
