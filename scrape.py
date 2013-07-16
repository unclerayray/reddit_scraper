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
from sanitize import sanitize

REDDIT_API_SLEEP_TIME = 2.50

def download_and_save(url, filename):
    """Saves the data at a given URL to a given local filename."""
    data = urlopen(url).read()
    with open(filename, mode='w') as output:
        output.write(data)
 
def main():
    ## Parse settings. TODO: allow argparse
    settings = eval(open('settings.txt', 'r').read())
    user_agent = settings['user_agent']
    image_extensions = settings['extensions']
    subreddits_dictionary = settings['subreddits']
    store_log = settings['store_log']
    alert = lambda s: print(s) if settings['verbose'] else None
    
    alert("Beginning web scrape.")
    alert('Getting user agent...')
    r = praw.Reddit(user_agent=user_agent)
    alert('Got user agent.')

    ## Used for percent-completion alerts.
    total_n = sum(len(v) for v in SUBREDDITS.values())
    n_so_far = 0.

    for base_dir, subreddits_for_dir in subreddits_dictionary.iteritems():
        for subreddit in subreddits_for_dir:
            subreddit_dir = os.path.join(base_dir, subreddit)
            if not os.path.exists(subreddit_dir):
                alert('Making %s' % subreddit_dir)
                os.makedirs(subreddit_dir)

            ## The API call
            submissions = r.get_subreddit(subreddit).get_top_from_day(limit=5)

            alert('/r/%s' % subreddit)
            for sub in submissions:
                url = sub.url
                alert('url is %s' % url)
                if any(sub.url.lower().endswith(ext.lower()) for ext in image_extensions):
                    alert('Found a picture.')
                    votes = '+%s,-%s' % (sub.ups, sub.downs)
                    extension = url.split('.')[-1]
                    alert('Extension is %s' % extension)
                    title = sanitize(sub.title) # Remove illegal characters
                    if title.endswith('.'): title = title[:-1] # Fix foo..jpg

                    local_filename = os.path.join(subreddit_dir, '%s.%s' % (title, extension))
                    alert('Saving to %s' % local_filename)

                    if store_log:
                        with open(os.path.join(base_dir, 'update.log'), 'a') as output:
                            print >> output, '%s|%s|%s|%s' % (datetime.datetime.now(), local_filename, votes, url)
                    download_and_save(url, local_filename)

            n_so_far += 1
            percent = int((100 * n_so_far) / total_n)
            alert("%d percent complete." % percent)

            sleep(REDDIT_API_SLEEP_TIME) # Avoid offending the Reddit API Gods!)
    alert("Completed web scrape.")  

if __name__ == '__main__':
    main()
