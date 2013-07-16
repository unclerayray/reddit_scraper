import praw

try:
    from alerts import say
except ImportError:
    pass # Not using OS X

from time import sleep
import urllib
import os
import datetime
now = datetime.datetime.now
from sanitize import sanitize

SETTINGS = eval(open('settings.txt').read())
USER_AGENT = SETTINGS['user_agent']
IMAGE_EXTENSIONS = SETTINGS['extensions']

def _print_indented(s, tabs=1):
    print ''.join(['\t'*tabs, s])

def save_to(url, filename):
    data = urllib.urlopen(url).read()
    with open(filename, mode='w') as output:
        output.write(data)
 
def main():
    say("Beginning web scrape.")
    print 'Getting user agent...',
    r = praw.Reddit(user_agent=USER_AGENT)
    print 'done'

    total_n = sum(len(v) for v in SUBREDDITS.values())
    n_so_far = 0.

    for base_dir, reddits in SUBREDDITS.iteritems():
        for reddit in reddits:
            subreddit_dir = os.path.join(base_dir, reddit)
            if not os.path.exists(subreddit_dir):
                print 'Making', subreddit_dir
                os.makedirs(subreddit_dir)

            ## The actual API call
            submissions = r.get_subreddit(reddit).get_top_from_day(limit=5)
            ##

            print '/r/%s' % reddit
            for sub in submissions:
                url = sub.url
                if any(sub.url.lower().endswith(ext.lower()) for ext in IMAGE_EXTENSIONS):
                    _print_indented('Found a picture.')
                    votes = '%s|%s' % (sub.ups, sub.downs)
                    _print_indented('url is %s' % url)
                    extension = url.split('.')[-1]
                    _print_indented('Extension is %s' % extension)

                    title = sanitize(sub.title)
                    if title.endswith('.'): title = title[:-1]

                    local_filename = os.path.join(subreddit_dir, '%s.%s' % (title, extension))
                    _print_indented('Saving to %s' % local_filename)

                    with open(os.path.join(base_dir, 'update.log'), 'a') as output:
                        print >> output, '%s|%s|%s|%s' % (now(), local_filename, votes, url)
                    save_to(url, local_filename)

                    print

            n_so_far += 1
            percent = int((100 * n_so_far) / total_n)
            if percent < 100:
                say("%d percent complete." % percent)

            sleep(2.5) # Avoid offending the Reddit API Gods!)
    say("Completed web scrape.")
        

if __name__ == '__main__':
    main()
