import os
import json

class Settings(object):
    basename = 'config.json'
    def __init__(self, directory=None):
        self.directory = self._get_directory(directory)
        self.data = self._init_data()

    def _init_data(self):
        """Load data or, create new data if there is no save file."""
        if os.path.exists(self.filename):
            self.load()
        else:
            self.reset()
        return self.data
        
    def _get_directory(self, dirname):
        """Return the path of the directory, or the current dir if None."""
        if dirname is None:
            return os.curdir
        else:
            return dirname

    @property
    def filename(self):
        return os.path.join(self.directory, self.__class__.basename)

    @property
    def user_agent(self):
        return self.data['user_agent']

    @property
    def groupings(self):
        return self.data['groupings'].values()
    
    def reset(self, save=False):
        self.data = {"groupings": {},
                     "user_agent": 'User-Agent: daily subreddit top-submission scraper v0.1 by /u/bluquar'}

    def load(self):
        if not os.path.exists(self.filename):
            self.save()
        with open(self.filename) as f:
            try:
                self.data = self.parse(json.loads(f.read()))
            except ValueError:
                self.reset()

    def save(self):
        data_dict = dict(self.data)
        data_dict['groupings'] = [grouping.serial for grouping in self.groupings]
        with open(self.filename, 'w') as f:
            f.write(json.dumps(data_dict, indent=1))

    def parse(self, raw_data):
        groupings = raw_data['groupings']
        groupings = {grouping['directory_name']: Grouping(grouping) for grouping in groupings}
        raw_data['groupings'] = groupings
        return raw_data        

    def add_grouping(self, dirname):
        self.data['groupings'][dirname] = Grouping({'directory_name': dirname})

    def __getitem__(self, index):
        return self.data['groupings'][index]
    
class Grouping(object):
    def __init__(self, data):
        self.data = {'directory_name': None,
                     'subdir_per_subreddit': True,
                     'enabled': True,
                     'subreddits': []}
        self.data.update(data)
        self.parse_subreddits()

    def parse_subreddits(self):
        subs = self.data['subreddits']
        subs = {sub['subreddit_name']: Subreddit(sub) for sub in subs}
        self.data['subreddits'] = subs

    def add_subreddit(self, subname):
        self.data['subreddits'][subname] = Subreddit({'subreddit_name': subname})

    def dirname_for(self, subreddit):
        if self.subdir_per_subreddit:
            return os.path.join(self.name, subreddit.name)
        else:
            return self.name
        
    @property
    def serial(self):
        s = dict(self.data)
        s['subreddits'] = [sub.data for sub in s['subreddits'].itervalues()]
        return s

    @property
    def subreddits(self):
        return self.data['subreddits'].values()

    @property
    def name(self):
        return self.data['directory_name']

    @property
    def enabled(self):
        return self.data['enabled']

    @property
    def subdir_per_subreddit(self):
        return self.data['subdir_per_subreddit']

    def __getitem__(self, index):
        return self.data['subreddits'][index]

class Subreddit(object):
    def __init__(self, data):
        self.data = {'subreddit_name': None,
                     'num_files': 0,
                     'file_types': ['JPG', 'PNG', 'GIF'],
                     'last_scraped': 'Never'}
        self.data.update(data)

    @property
    def name(self):
        return self.data['subreddit_name']
    @property
    def num_files(self):
        return self.data['num_files']
    @property
    def file_types(self):
        return self.data['file_types']
    @property
    def last_scraped(self):
        return self.data['last_scraped']
