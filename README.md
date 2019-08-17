# crackwatch
crackwatch monitors a password cracking process and posts updates to slack

requirements:    slack webhook url (https://api.slack.com/incoming-webhooks)
usage:           ./crackwatch
with arguments:  ./crackwatch <PROCESS> <POTFILE> <INTERVAL>
example:         ./crackwatch hashcat hashcat.pot 60