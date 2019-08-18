# crackwatch
Crackwatch monitors a specified password cracking process and posts periodic updates to slack.
I've used it successfully with hashcat and mdxfind, but it should be able to work with others, like john.
Be sure to specify the full path to the potfile, if it's not in the same directory. The interval is the
length of time between updates, in minutes. For example, `60` would post updates every hour. Your webhook url 
must be added to the `webhook_url` variable in crackwatch.py.

This can be adapted to pretty much any webhook. PRs are welcome.

---

requirements: slack webhook url (https://api.slack.com/incoming-webhooks)
              Once you have obtained a webhook url, add it to crackwatch.py

usage:        `python3 crackwatch.py -p <process> -f <potfile> -i <interval>`

              <process> is the process you want to monitor
              <potfile> is the output file from that process
              <interval> is how often (in minutes) you want slack updates

example:  `python3 crackwatch hashcat hashcat.pot 60`

note: there is a bash version on the master branch