__doc__ = """Scrapes images linked to from specified subreddits."""

try:
    import praw
except ImportError:
    print "Unable to find praw. see https://github.com/praw-dev/praw"
    raise

from time import sleep
from urllib import urlopen
import os
import datetime
import string

_REDDIT_API_SLEEP_TIME = 2.50
_VALID_CHARS = frozenset(''.join(("-_.() ", string.ascii_letters, string.digits)))

def sanitize(s):
    return ''.join(c for c in s if c in _VALID_CHARS)

def download_and_save(url, filename):
    """Saves the data at a given URL to a given local filename."""
    data = urlopen(url).read()
    with open(filename, mode='w') as output:
        output.write(data)
 
def main():
    ## Parse settings. TODO: allow argparse
    settings = eval(open('settings.txt', 'r').read())
    image_extensions = settings['extensions']
    store_log = settings['store_log']
    alert = lambda s: print(s) if settings['verbose'] else None
    
    alert("Beginning web scrape.")
    r = praw.Reddit(user_agent=settings['user_agent'])
    alert('Got user agent.')

    ## Used for percent-completion alerts.
    total_n = sum(len(v) for v in settings['subreddits'].values())
    n_so_far = 0.

    for base_dir, subreddits_for_dir in settings['subreddits'].iteritems():
        for subreddit in subreddits_for_dir:
            subreddit_dir = os.path.join(base_dir, subreddit)
            if not os.path.exists(subreddit_dir):
                alert('Making %s' % subreddit_dir)
                os.makedirs(subreddit_dir)

            ## The API call
            submissions = r.get_subreddit(subreddit).get_top_from_day(limit=5)

            alert(''.join(('/r/', subreddit)))
            for sub in submissions:
                url = sub.url
                alert(''.join(('url is ', url))
                if any(sub.url.lower().endswith(ext.lower()) for ext in image_extensions):
                    alert('Found a picture.')
                    votes = '+%s,-%s' % (sub.ups, sub.downs)
                    extension = url.split('.')[-1]
                    alert(''.join(('Extension is ', extension)))
                    title = sanitize(sub.title) # Remove illegal characters
                    if title.endswith('.'): title = title[:-1] # Fix foo..jpg

                    local_filename = os.path.join(subreddit_dir, '%s.%s' % (title, extension))
                    alert(''.join(('Saving to ', local_filename)))

                    if store_log:
                        with open(os.path.join(base_dir, 'update.log'), 'a') as output:
                            print >> output, '%s|%s|%s|%s' % (datetime.datetime.now(), local_filename, votes, url)
                    download_and_save(url, local_filename)

            n_so_far += 1
            percent = int((100 * n_so_far) / total_n)
            alert("%d percent complete." % percent)

            sleep(_REDDIT_API_SLEEP_TIME) # Avoid offending the Reddit API Gods!
    alert("Completed web scrape.")  

if __name__ == '__main__':
    main()
