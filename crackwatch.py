#! /usr/bin/python3
#
# about:  crackwatch watches your cracking process and posts progress updates to slack
# requirements:  slack webhook url (https://api.slack.com/incoming-webhooks)
# usage:  python3 crackwatch.py -p <process> -f <potfile> -i <interval>
#       <process> is the process you want to monitor
#       <potfile> is the output file from that process
#       <interval> is how often (in minutes) you want slack updates
# example:  python3 crackwatch hashcat hashcat.pot 60
#
# author: 0xoperant
# 	based on https://github.com/secgroundzero/hashslack

import sys, getopt, subprocess, json, time
from urllib import request, parse

# provide your webhook here
webhook_url = ''

# slack post function
def post(text):
    post = {"text": "{0}".format(text)}
    try:
        json_data = json.dumps(post)
        req = request.Request(webhook_url,
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'})
        resp = request.urlopen(req)
    except Exception as em:
        print ("Error: " + str(em))

def main(argv):
    # gather required arguments
    try:
       opts, args = getopt.getopt(argv,"hu:p:f:i:",["uurl=","pprocess=","fpotfile=","iinterval="])
    except getopt.GetoptError:
        print ('crackwatch.py -p <process> -f <potfile> -i <interval>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
           print ('crackwatch.py -p <process> -f <potfile> -i <interval>')
           sys.exit()
        elif opt in ("-p", "--pprocess"):
            process = arg
        elif opt in ("-f", "--fpotfile"):
            potfile = arg
        elif opt in ("-i", "--iinterval"):
            interval = int(arg)
    
    # check to see if the process is running
    if (subprocess.getoutput('pgrep ' + process)) != '':
        with open(potfile) as l:
            hashes = int(sum(1 for _ in l))
        print ('Monitoring ' + process + '! I will tell you when there are new hashes. Otherwise, I will post an update every ' + str(interval) + ' minutes.')
        post ("New Session - Potfile: " + str(hashes) + " hashes. Unless there are new hashes, I will post an update in " + str(interval) + " minutes.")
        count = 0

        # start monitoring loop
        while (subprocess.getoutput('pgrep ' + process)) != '':
            time.sleep(60)
            with open(potfile) as l:
                newhashes = int(sum(1 for _ in l))
            if newhashes > hashes:
                print ("New cracks! Posting update to slack.")
                post ("New cracks! - Potfile: " + str(newhashes) + " hashes.")
                hashes = newhashes
            else:
                count += 1
                if count == interval:
                    print ("No new cracks yet. Posting update to slack.")
                    post ("No new cracks yet. - Potfile: " + str(newhashes) + " hashes.")
                    count = 0
        else:
            print (process + " session completed!")
            post (process + " session completed! Hashes cracked: " + str(hashes))

    # error if the requested process isn't running
    else:
        print (process + " is not running! use -h for help.")

if __name__ == "__main__":
   main(sys.argv[1:])