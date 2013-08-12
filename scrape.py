__doc__ = """Scrapes images linked to from specified subreddits."""

try:
    import praw
except ImportError:
    print "Unable to find praw. see https://github.com/praw-dev/praw"
    raise()

from time import sleep
from urllib import urlopen
import os
import sys
import datetime
import string

_REDDIT_API_SLEEP_TIME = 2.50
_VALID_CHARS = frozenset(''.join(("-_.() ", string.ascii_letters, string.digits)))

def sanitize(s, default_name="image"):
    sanitized = ''.join(c for c in s if c in _VALID_CHARS)
    return sanitized if sanitized else default_name # Use default if string is empty.

def unique(filename):
    """Returns a guaranteed-unique version of a given filename."""
    if not os.path.exists(filename):
        return filename
    else:
        parts = filename.split('.')
        parts.insert(-1, '%d') # Put a number before the extension.
        filename_fmt = '.'.join(parts)
        num = 0
        while os.path.exists(filename_fmt % num):
            num += 1
        return filename_fmt % num

def download_and_save(url, filename):
    """Saves the data at a given URL to a given local filename."""
    data = urlopen(url).read()
    with open(filename, mode='w') as output:
        output.write(data)

def fetch_image(submission, directory, store_log, base_dir):
    votes = '+%s,-%s' % (submission.ups, submission.downs)
    url = submission.url
    extension = url.split('.')[-1]
    title = sanitize(submission.title) # Remove illegal characters
    if title.endswith('.'): title = title[:-1] # Fix foo..jpg
    local_filename = unique(os.path.join(directory, '%s.%s' % (title, extension)))
    download_and_save(url, local_filename)

def scrape(settings):
    
    r = praw.Reddit(user_agent=settings.user_agent)

    for grouping in settings.groupings:
        for subreddit in grouping.subreddits:
            dirname = grouping.dirname_for(subreddit)
            if not os.path.exists(dirname):

                os.makedirs(dirname)
            extensions = set(subreddit.file_types)

            submissions = r.get_subreddit(subreddit.name).get_top_from_day(limit=5)
            for sub in submissions:
                url = sub.url
                if any(sub.url.lower().endswith(ext.lower()) for ext in image_extensions):
                    fetch_image(sub, dirname, store_log)  
                    
            sleep(_REDDIT_API_SLEEP_TIME) # Avoid offending the Reddit API Gods!


