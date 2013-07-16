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

def download_and_save(url, filename):
    data = urlopen(url).read()
    with open(filename, mode='w') as output:
        output.write(data)
 
def main():
    settings = eval(open('settings.txt').read())
    user_agent = settings['user_agent']
    image_extensions = settings['extensions']
    subreddits = settings['subreddits']
    store_log = settings['store_log']
    alert = lambda s: print(s) if settings['verbose'] else None
    
    alert("Beginning web scrape.")
    alert('Getting user agent...')
    r = praw.Reddit(user_agent=user_agent)
    alert('Got user agent.')

    total_n = sum(len(v) for v in SUBREDDITS.values())
    n_so_far = 0.

    for base_dir, reddits_for_dir in subreddits.iteritems():
        for reddit in reddits_for_dir:
            subreddit_dir = os.path.join(base_dir, reddit)
            if not os.path.exists(subreddit_dir):
                alert('Making %s' % subreddit_dir)
                os.makedirs(subreddit_dir)

            ## The API call
            submissions = r.get_subreddit(reddit).get_top_from_day(limit=5)

            alert('/r/%s' % reddit)
            for sub in submissions:
                url = sub.url
                alert('url is %s' % url)
                if any(sub.url.lower().endswith(ext.lower()) for ext in IMAGE_EXTENSIONS):
                    alert('Found a picture.')
                    votes = '%s|%s' % (sub.ups, sub.downs)
                    extension = url.split('.')[-1]
                    alert('Extension is %s' % extension)
                    title = sanitize(sub.title)
                    if title.endswith('.'): title = title[:-1]

                    local_filename = os.path.join(subreddit_dir, '%s.%s' % (title, extension))
                    alert('Saving to %s' % local_filename)

                    if store_log:
                        with open(os.path.join(base_dir, 'update.log'), 'a') as output:
                            print >> output, '%s|%s|%s|%s' % (datetime.datetime.now(), local_filename, votes, url)
                    download_and_save(url, local_filename)

            n_so_far += 1
            percent = int((100 * n_so_far) / total_n)
            alert("%d percent complete." % percent)

            sleep(2.5) # Avoid offending the Reddit API Gods!)
    alert("Completed web scrape.")  

if __name__ == '__main__':
    main()
