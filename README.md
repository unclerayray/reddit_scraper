Reddit Scraper
=======

Configure by simply editing settings.txt, and you'll be ready to run scrape.py.

Choose which subreddits you want to scrape from. The scraper will take the top 5 highest rated posts on those subreddits from today, and save any images to the specified directory. For example, you could scrape the top posts from /r/wallpapers into your wallpaper folder. Set up a cron job to do this every day and you will get a new wallpaper every day :)

TODO:

* Allow greater configuration in settings.txt

Uses Python Reddit API Wrapper: https://github.com/praw-dev/praw
`pip install praw`

Contact me: chrisbarker@cmu.edu

