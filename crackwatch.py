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

import os, sys, getopt, subprocess, json, time
from urllib import request, parse

# check the webhook url is set
try:
    webhook_url = os.environ['WEBHOOK_URL']
except KeyError:
    try:
        os.environ['WEBHOOK_URL'] = input('Please enter your webhook url: ')
        webhook_url = os.environ['WEBHOOK_URL']
    except ValueError:
        print ("Error: you need to provide a webhook url", file=sys.stderr)
        sys.exit(1)

# slack post function
def post(text):
    post = {"text": "{0}".format(text)}
    try:
        json_data = json.dumps(post)
        req = request.Request(webhook_url, data=json_data.encode('ascii'), headers={'Content-Type': 'application/json'})
        resp = request.urlopen(req)
    except Exception as em:
        print ("Error: " + str(em), file=sys.stderr)

# process checking function
def getpid(process):
    try:
        pid = int(subprocess.check_output(['pgrep', process], encoding='UTF-8'))
    except subprocess.CalledProcessError as e:
        print (e.output, file=sys.stderr)
        pid = 0
    return pid

# count them cracks
def gethashes(potfile):
    try:
        with open(potfile) as l:
            cracks = int(sum(1 for _ in l))
    except IOError as e:
            print (e, file=sys.stderr)
    return cracks
        
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
    
    # check to see if the process exists
    if getpid(process) != 0:
        hashes = gethashes(potfile)
        print ('Monitoring ' + process + '! I will tell you when there are new hashes. Otherwise, I will post an update every ' + str(interval) + ' minutes.')
        post ("New " + process + " session! Watching for hashes in " + potfile +": " + str(hashes) + " hashes currently. Unless there are new hashes, I will post an update in " + str(interval) + " minutes.")
        count = 0

        # start monitoring loop
        while getpid(process) != 0:
            time.sleep(60)
            newhashes = gethashes(potfile)
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