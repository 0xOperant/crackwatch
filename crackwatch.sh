#!/bin/bash
#
# about:  crackwatch watches your cracking process and posts progress updates to slack
# requirements:  slack webhook url (https://api.slack.com/incoming-webhooks)
# usage:  ./crackwatch
# with arguments:  ./crackwatch <PROCESS> <POTFILE> <INTERVAL>
# example:  ./crackwatch hashcat hashcat.pot 60
#
# author: 0xoperant
# 	based on https://github.com/secgroundzero/hashslack

# provide slack webhook url
webhook_url="" 

# prompt for webhook url if not set above
if [ -z ${webhook_url} ]; then 
	read -p "Input slack webhook url: " webhook_url
	webhook_url=${webhook_url}
fi

# prompt for process to watch, if not specified
if [[ "$1" ]]; then
	watch_process=$1
else
	read -p "What cracker are you running? [hashcat] " watch_process
	watch_process=${watch_process:-hashcat}
fi

# prompt for potfile to watch, if not specified
if [[ "$2" ]]; then
	pot_file=$2
	if [ ! -f $pot_file ]; then
		touch $pot_file
	fi
else
	read -p "What file should I monitor? [hashcat.potfile] " pot_file
	pot_file=${pot_file:-hashcat.potfile}
	if [ ! -f $pot_file ]; then
		touch $pot_file
	fi
fi

# prompt for alert interval
if [[ "$3" ]]; then
	update=$3
else
	read -p "How many minutes between status updates? [60] " update
	update=${update:-60}
fi

# initialize counter
count=0

# check to see if the process is running
if pgrep -x $watch_process > /dev/null; then
	hashes=$(wc -l < $pot_file)
        echo "Monitoring $watch_process! I'll tell you when there are new hashes. Otherwise, I'll post an update every $update minutes."
	curl -s -X POST -H 'Content-type: application/json' --data '{"text":"New Session - Potfile: '$hashes' hashes. Unless there are new hashes, I will post an update in '$update' minutes."}' $webhook_url > /dev/null

    # start the loop
	while true; do
		sleep 1m
		if pgrep -x $watch_process > /dev/null; then
			newhashes=$(wc -l < $pot_file)
			if [ "$newhashes" -gt "$hashes" ]; then
				echo "New cracks! Posting update to slack."
				curl -s -X POST -H 'Content-type: application/json' --data '{"text":"New cracks! - Potfile: '$newhashes' hashes."}' $webhook_url > /dev/null
				hashes=$newhashes
		        else
				count=$((count+1))
				if [ $count -eq $update ]; then
					echo "No new cracks yet. Posting update to slack."
					curl -s -X POST -H 'Content-type: application/json' --data '{"text":"No new cracks yet. - Potfile: '$newhashes' hashes."}' $webhook_url > /dev/null
					count=0
				fi
			fi
		else
			echo "$watch_process session completed."
			curl -s -X POST -H 'Content-type: application/json' --data '{"text":"$watch_process task completed. '$hashes' hashes cracked!"}' $webhook_url > /dev/null
			break
		fi
	done
else

# exit if the process isn't running
echo "$watch_process is not running!"

fi