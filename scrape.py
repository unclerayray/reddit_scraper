"""Scrape images linked to from specified subreddits."""

try:
    import praw
except ImportError:
    print "Unable to find praw. see https://github.com/praw-dev/praw"
    raise

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
    """Return a guaranteed-unique version of a given filename."""
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
    """Save the data at a given URL to a given local filename."""
    data = urlopen(url).read()
    with open(filename, mode='w') as output:
        output.write(data)

def fetch_image(submission, directory, store_log, alert, base_dir):
    alert('Found a picture.')
    votes = '+%s,-%s' % (submission.ups, submission.downs)
    url = submission.url
    extension = url.split('.')[-1]
    alert(''.join(('Extension is ', extension)))
    title = sanitize(submission.title) # Remove illegal characters
    if title.endswith('.'): title = title[:-1] # Fix foo..jpg
    local_filename = unique(os.path.join(directory, '%s.%s' % (title, extension)))
    alert(''.join(('Saving to ', local_filename)))
    if store_log:
        with open(os.path.join(base_dir, 'update.log'), 'a') as output:
            print >> output, '%s|%s|%s|%s' % (datetime.datetime.now(), local_filename, votes, url)
    download_and_save(url, local_filename)

def scrape(settings):
    image_extensions = settings['extensions']
    store_log = settings['store_log']
    alert = lambda s: sys.stdout.write(s+'\n') if settings['verbose'] else None
    
    alert("Beginning web scrape.")
    r = praw.Reddit(user_agent=settings['user_agent'])
    alert('Got user agent.')

    ## Used for percent-completion alerts.
    total_n = sum(len(v) for v in settings['subreddits'].values())
    n_so_far = 0.

    for base_dir, subreddits_for_dir in settings['subreddits'].iteritems():
        for subreddit in subreddits_for_dir:
            alert(''.join(('/r/', subreddit)))
            subreddit_dir = os.path.join(base_dir, subreddit)
            if not os.path.exists(subreddit_dir):
                alert('Making %s' % subreddit_dir)
                os.makedirs(subreddit_dir)
                
            ## The API call
            submissions = r.get_subreddit(subreddit).get_top_from_day(limit=5)
            
            for sub in submissions:
                url = sub.url
                alert(''.join(('url is ', url)))
                if any(sub.url.lower().endswith(ext.lower()) for ext in image_extensions):
                    fetch_image(sub, subreddit_dir, store_log, alert, base_dir)   
                    
            n_so_far += 1
            percent = int((100 * n_so_far) / total_n)
            alert("%d percent complete." % percent)

            sleep(_REDDIT_API_SLEEP_TIME) # Avoid offending the Reddit API Gods!
    alert("Completed web scrape.")  


def main():
    ## Parse settings. TODO: allow argparse
    settings = eval(open('settings.txt', 'r').read())
    scrape(settings)

if __name__ == '__main__':
    main()
