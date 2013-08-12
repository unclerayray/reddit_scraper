# gui.py

import Tkinter
import functools
wraps = functools.wraps

import settings
import scrape
import itertools

def gui(fn):
    @wraps(fn)
    def updater(self, *args, **kwargs):
        val = fn(self, *args, **kwargs)
        self.update_gui()
        return val
    return updater
                
class ScraperWindow(object):
    def __init__(self):
        self.root = self.get_root()
        self.state = GUIState()
        self.settings = settings.Settings()
        self.add_elements()
        self.update_gui()
        self.root.after(100, self.center_window)
        self.root.mainloop()

    def get_root(self):
        """Create a new window."""
        root = Tkinter.Tk()
        root.title("Reddit Scraper")
        return root
        
    def center_window(self):
        w = float(self.root.winfo_screenwidth())
        h = float(self.root.winfo_screenheight())
        rootsize = tuple(int(i) for i in self.root.geometry().split('+')[0].split('x'))
        x = w/2 - rootsize[0]/2
        y = h/2 - rootsize[1]/2
        self.root.geometry("%dx%d+%d+%d" % (rootsize + (x, y)))

    def scrape(self):
        scrape.scrape(self.settings)

    def add_elements(self):
        root = self.root
        self.add_groupings_pane(root)
        self.add_subreddits_pane(root)
        self.add_details_pane(root)

    def add_groupings_pane(self, root):
        pane = Tkinter.Frame(root)
        # List of directories,
        # Add directory button,
        grouping_buttons = [("Add Directory", self.add_directory, 0, 0)]
        for text, command, row, col in grouping_buttons:
            Tkinter.Button(pane, text=text, command=command).grid(row=row, column=col)

        # Reomve directory button,
        # Enable/Disable button
        # Scrape all button
        # Load/Save
        pane.grid(row=0, column=0)

    def add_subreddits_pane(self, root):
        pane = Tkinter.Frame(root)

        # List of subreddits,
        self.subreddit_listbox = Tkinter.Listbox(pane)
        self.subreddit_listbox.grid(row=0, column=0)
        self.subreddit_listbox.insert(Tkinter.END, '<Subreddits>')
        
        # Add subreddit button
        # Remove subreddit button
        # Create folder for each subreddit (checkbox)
        # Scrape all button
        pane.grid(row=0, column=1)

    def add_details_pane(self, root):
        pane = Tkinter.Frame(root)
        # Subreddit name
        # Number of files to download (INC/DEC)
        # File types to include (list box?) (ADD/REM)
        # Enable/Disable button (CHECK BOX)
        # Last scraped (LABEL)
        # Open folder in finder/explorer (BUTTON)
        # Scrape now button
        pane.grid(row=0, column=2)
        
    def update_gui(self):
        print 'updating!'

    @gui
    def add_subreddit(self):
        # This should just be:
        # Settings[self.state.grouping].add_subreddit(...)
        # These things should directly change SETTINGS and the state variables
        self.remove_sr_placeholder()
        text = self.entry_field.get()
        self.listbox.insert(Tkinter.END, text)

    @gui
    def remove_subreddit(self):
        pass

    @gui
    def save(self):
        pass

    @gui
    def load(self):
        self.settings.load()
        self.update_gui()

    @gui
    def add_directory(self):
        print 'hello'
        pass

class GUIState(object):
    def __init__(self, data=None):
        default = {'grouping': None,
                   'subreddit': None}
        if data is not None:
            default.update(data)
        self.__dict__.update(default)
