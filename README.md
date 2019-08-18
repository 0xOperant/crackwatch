# crackwatch
Crackwatch monitors a specified password cracking process and posts periodic updates to slack.
I've used it successfully with hashcat and mdxfind, but it should be able to work with others, like john.
Be sure to specify the full path to the potfile, if it's not in the same directory. The interval is the
length of time between updates, in minutes. For example, `60` would post updates every hour. The webhook url can be
provided as an argument, or added to the `webhook_url` variable in crackwatch.sh.

This can be adapted to pretty much any webhook. PRs are welcome.

Note: there is a python3 version in the `python` branch.

---

requirements:    slack webhook url (https://api.slack.com/incoming-webhooks)

usage:           `./crackwatch`

with arguments:  `./crackwatch <PROCESS> <POTFILE> <INTERVAL>`

example:         `./crackwatch hashcat hashcat.pot 60`