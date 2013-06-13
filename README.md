# twitwatch

Twitwatch is a tool to listen to Twitter's streaming API and store tweets.


## Requirements
Twitwatch needs a recent version of Python 2, Python requests (&gt;1.0), and
requests-oauthlib (&gt;0.3.2).

## Usage
Authenticating is trickier now that you are required to use oauth1.  First, you
will need a Twitter Application. You can create one at
https://dev.twitter.com/apps . When you create the application, it will give
you a consumer key and consumer secret. Next, you should click "Create my
access token" at the bottom of the page, which will create the access token and
access token secret that you will also need.  Yes, you really do need four
different strings to identify yourself to Twitter.

Copy settings_example.py to settings.py. Change the username, password, filter,
and directory to store files in.  You can create additional dictionaries in
settings if you want to run multiple crawlers.  Then you can run the crawler by
running `crawl.py` followed by the name of the field in settings to use.  In
the example settings, you can start the link crawler by running this command:

    ./crawl.py link

## Notes
The crawler process automatically kills the process and restarts it every 15
minutes. This is a crude way to guarantee that the crawler starts working again
even if the connection to Twitter breaks down.

This is based on @bde's TwitterStreamSaver, but it uses the Requests library
instead of libcurl. The requests code is based on an example from Requests'
documentation.
