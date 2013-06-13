#!/usr/bin/env python

import datetime
import logging
import os
import signal
import sys
import time

import requests
import requests_oauthlib

# you will need to make settings.py based on settings_example.py
from settings import settings


def store_tweets(config, output_file):
    """ read tweets from Twitter's streaming API and write them to a file """
    filter_url = 'https://stream.twitter.com/1/statuses/filter.json'
    headerauth = requests_oauthlib.OAuth1(
            config['consumer_key'], config['consumer_secret'],
            config['token_key'], config['token_secret'],
            signature_type='auth_header',
            )
    r = requests.post(
            config.get('stream_url',filter_url),
            data=config.get('params',None),
            auth=headerauth,
            stream=True,
            )

    count = 0
    for line in r.iter_lines():
        if line: # filter out keep-alive new lines
            print>>output_file, line
            count +=1
            if count%1000==0:
                logging.info("saved %d tweets",count)


def main():
    """ create a watchdog process to monitor the twitter crawler """
    label = sys.argv[1]
    config = settings[label]
    log_dir = config.get('logs') or config['directory']
    logging.basicConfig(
        filename=os.path.join(log_dir,"%s.%d.log"%(label,os.getpid())),
        format="%(levelname)s:%(module)s:%(asctime)s:%(message)s",
        level=logging.INFO,
    )

    logging.info("starting to crawl %s",label)
    while True:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = "%s/%s.%s.txt"%(config['directory'],label,date_str)

        logging.info("creating child for %s from %d",filename,os.getpid())

        cpid = os.fork()
        if cpid == 0:
            # child
            logging.info("writing to new file: %s",filename)
            try:
                with open(filename,'w',1) as f:
                    store_tweets(config,f)
            except:
                logging.exception("crash in child proc")
                raise
            logging.info("unexpected death in %d",os.getpid())
            break
        else:
            # parent
            time.sleep(config.get('time_length',15*60))
            logging.info("killing %d",cpid)
            os.kill(cpid, signal.SIGTERM)
            os.waitpid(cpid, 0)


if __name__=='__main__':
    main()
