# twitwatch

Twitwatch is a tool to listen to Twitter's streaming API and store tweets.


## Requirements
Twitwatch needs a recent version of Python 2 and the Python requests library.

## Usage
Copy settings_example.py to settings.py. Change the username, password, filter,
and directory to store files in.  You can create additional dictionaries in
settings if you want to run multiple crawlers.  Then you can run the crawler by
running `crawl.py` followed by the name of the field in settings to use.  In
the example settings, you can start the crawler by running this command:

    ./crawl.py aggies

## Notes
The crawler process automatically kills the process and restarts it every 15
minutes. This is a crude way to guarantee that the crawler starts working again
even if the connection to Twitter breaks down.

This is based on @bde's TwitterStreamSaver, but it uses the Requests library
instead of libcurl. The requests code is based on an example from Requests'
documentation.
