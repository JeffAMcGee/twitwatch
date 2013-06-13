#!/usr/bin/env python
from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs

"""
This is a tool to create Twitter oauth tokens for a user. It is based on the
requests_oauthlib documentation. You only need this if you create an application
with one user and you want to crawl tweets as a different user.
"""

print "First, create an application at https://dev.twitter.com/apps"

client_key = raw_input('Please paste the consumer key: ')
client_secret = raw_input('Please paste the consumer secret: ')

oauth = OAuth1(client_key, client_secret=client_secret)
request_token_url = 'https://api.twitter.com/oauth/request_token'
r = requests.post(url=request_token_url, auth=oauth)

credentials = parse_qs(r.content)
resource_owner_key = credentials.get('oauth_token')[0]
resource_owner_secret = credentials.get('oauth_token_secret')[0]

authorize_url = 'https://api.twitter.com/oauth/authorize?oauth_token='
authorize_url = authorize_url + resource_owner_key
print 'Please go here and authorize: ', authorize_url
verifier = raw_input('Please paste the verifier: ')

oauth = OAuth1(client_key,
               client_secret=client_secret,
               resource_owner_key=resource_owner_key,
               resource_owner_secret=resource_owner_secret,
               verifier=verifier)
access_token_url = 'https://api.twitter.com/oauth/access_token'
r = requests.post(url=access_token_url, auth=oauth)

credentials = parse_qs(r.content)
token_key = credentials.get('oauth_token')[0]
token_secret = credentials.get('oauth_token_secret')[0]

template = """
Use this in settings.py:

        consumer_key = '%s',
        consumer_secret = '%s',
        token_key = '%s',
        token_secret = '%s',
"""
print template%( client_key, client_secret, token_key, token_secret )
