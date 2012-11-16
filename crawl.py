#!/usr/bin/env python

import datetime
import os
import signal
import sys
import time

import requests

# you will need to make settings.py based on settings_example.py
from settings import settings


def store_tweets(config, output_file):
    # read tweets from Twitter's streaming API and write them to a file.
    filter_url = 'https://stream.twitter.com/1/statuses/filter.json'
    r = requests.post(
            config.get('url',filter_url),
            data=config.get('params',None),
            auth=(config['username'],config['password']),
            )

    count = 0
    for line in r.iter_lines():
        if line: # filter out keep-alive new lines
            print>>output_file, line
            count +=1
            if count%100==0:
                print count

def main():
    label = sys.argv[1]
    config = settings[label]

    while True:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = "%s/%s.%s.txt"%(config['directory'],label,date_str)

        cpid = os.fork()
        if cpid == 0:
            # child
            print "starting on %s"%filename
            with open(filename,'w',1) as f:
                store_tweets(config,f)
        else:
            # parent
            time.sleep(config.get('time_length',15*60))
            os.kill(cpid, signal.SIGTERM)
            os.waitpid(cpid, 0)


if __name__=='__main__':
    main()
