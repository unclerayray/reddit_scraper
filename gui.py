# gui.py

import Tkinter
import tkFileDialog
import tkSimpleDialog
import tkMessageBox

import functools
wraps = functools.wraps

import settings
import scrape
import itertools

SELECTION_COLOR = '#9999ff'
BLANK_COLOR = '#ffffff'

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
        self.start_timer()
        self.root.mainloop()

    def start_timer(self):
        self.prev_state = self.state.tuple()
        self.root.after(100, self.timer)

    def timer(self):
        self.grouping_listbox.selection_clear(0, Tkinter.END)
        self.subreddit_listbox.selection_clear(0, Tkinter.END)
        if not self.prev_state == self.state.tuple():
            self.update_gui()
        self.prev_state = self.state.tuple()
        self.root.after(100, self.timer)

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

    def scrape_current_sub(self):
        scrape.scrape(self.settings, include_sub={self.state.subreddit})

    def add_elements(self):
        root = self.root
        self.add_groupings_pane(root)
        self.add_subreddits_pane(root)
        self.add_details_pane(root)

    def add_groupings_pane(self, root):
        pane = Tkinter.Frame(root)
        # List of directories,
        self.grouping_listbox = Tkinter.Listbox(pane)
        self.grouping_listbox.grid(row=0, column=0, columnspan=2, sticky=Tkinter.N)
        self.grouping_listbox.bind('<Button-1>', self.grouping_listbox_click)

        # Add directory button,
        add_dir_button = Tkinter.Button(pane, text="Add Directory", command=self.add_directory)
        add_dir_button.grid(row=1, column=0, sticky=Tkinter.W)

        # Reomve directory button,
        # Enable/Disable button
        # Scrape all button
        # Load/Save
        pane.grid(row=0, column=0)


    def add_subreddits_pane(self, root):
        pane = Tkinter.Frame(root)

        # List of subreddits,
        self.subreddit_listbox = Tkinter.Listbox(pane)
        self.subreddit_listbox.grid(row=0, column=0, columnspan=2, sticky=Tkinter.N)
        self.subreddit_listbox.bind('<Button-1>', self.subreddit_listbox_click)


        # Add subreddit button
        add_sub_button = Tkinter.Button(pane, text="Add Subreddit", command=self.add_subreddit)
        add_sub_button.grid(row=1, column=0, sticky=Tkinter.W)

        # Remove subreddit button
        # Create folder for each subreddit (checkbox)
        # Scrape all button
        pane.grid(row=0, column=1)

    def add_details_pane(self, root):
        pane = Tkinter.Frame(root, width=500)
        # Subreddit name
        self.subreddit_name_label = Tkinter.Label(pane, text='', anchor=Tkinter.N)
        self.subreddit_name_label.grid(row=0, column=0, columnspan=2)

        # Number of files to download (INC/DEC)
        self.number_of_files_label = Tkinter.Label(pane, text='Files to Download:')
        self.number_of_files_label.grid(row=1, column=0)

        self.number_of_files_entry = Tkinter.Entry(pane, width=3)
        self.number_of_files_entry.grid(row=1, column=1)

        # File types to include (list box?) (ADD/REM)
        self.file_types_label = Tkinter.Label(pane, text="Include these extensions:")
        self.file_types_label.grid(row=2, column=0, columnspan=2)
        
        self.file_types_listbox = Tkinter.Listbox(pane, height=5)
        self.file_types_listbox.grid(row=3, column=0, columnspan=2)

        # Enable/Disable button (CHECK BOX)
        # Last scraped (LABEL)
        # Open folder in finder/explorer (BUTTON)
        # Scrape now button
        self.scrape_now_button = Tkinter.Button(pane, text="Scrape Now", command=self.scrape_current_sub)
        self.scrape_now_button.grid(row=4, column=0, columnspan=2)
        
        pane.grid(row=0, column=2)

    def grouping_listbox_click(self, event):
        index = self.grouping_listbox.nearest(event.y)
        self.state.grouping = self.grouping_listbox.get(index)
        for i in xrange(self.grouping_listbox.size()):
            self.grouping_listbox.itemconfig(i, bg=BLANK_COLOR)
        self.grouping_listbox.itemconfig(index, bg=SELECTION_COLOR)
        event.widget.selection_clear(0, Tkinter.END)

    def subreddit_listbox_click(self, event):
        if self.grouping is None:
            return
        index = self.subreddit_listbox.nearest(event.y)
        self.state.subreddit = self.subreddit_listbox.get(index)
        for i in xrange(self.subreddit_listbox.size()):
            self.subreddit_listbox.itemconfig(i, bg=BLANK_COLOR)
        self.subreddit_listbox.itemconfig(index, bg=SELECTION_COLOR)
        event.widget.selection_clear(0, Tkinter.END)

    @property
    def grouping(self):
        if self.state.grouping is None: return None
        return self.settings[self.state.grouping]

    @property
    def subreddit(self):
        if self.state.subreddit is None: return None
        return self.grouping[self.state.subreddit]

    def update_gui(self):
        ## Grouping listbox
        desired_grouping_listbox = [group.shortname for group in self.settings.groupings]
        if not desired_grouping_listbox:
            desired_grouping_listbox = ['<Directories>']
        self._listbox_update(self.grouping_listbox, desired_grouping_listbox)
        #
        # Make the selected one a particular color
        #

        ## Subreddit listbox
        if self.grouping is None:
            desired_subreddit_listbox = ['<Subreddits>']
        else:
            desired_subreddit_listbox = [sub.name for sub in self.grouping.subreddits]
        if not desired_subreddit_listbox:
            desired_subreddit_listbox = ['<Subreddits>']
        self._listbox_update(self.subreddit_listbox, desired_subreddit_listbox)

        ## Details Frame
        if self.subreddit is not None:
            self.subreddit_name_label.config(text='/r/'+self.state.subreddit)
            desired_num = str(self.subreddit.num_files)
            if self.number_of_files_entry.get() != desired_num:
                self.number_of_files_entry.delete(0, Tkinter.END)
                self.number_of_files_entry.insert(0, desired_num)
            desired_filetypes = self.subreddit.file_types
            self._listbox_update(self.file_types_listbox, desired_filetypes)
        else:
            self.subreddit_name_label.config(text='')
            self.number_of_files_entry.delete(0, Tkinter.END)
            self._listbox_update(self.file_types_listbox, [])


    def _listbox_update(self, listbox, desired_values):
        current_values = listbox.get(0, Tkinter.END)
        to_remove = set(current_values) - set(desired_values)
        to_add = set(desired_values) - set(current_values)
        for item in to_remove:
            idx = listbox.get(0, Tkinter.END).index(item)
            listbox.delete(idx)
        for item in to_add:
            listbox.insert(Tkinter.END, item)


    @gui
    def add_subreddit(self):
        if self.grouping is None:
            tkMessageBox.askokcancel("", "Please select a directory first.")
        else:
            s = tkSimpleDialog.askstring("Add a Subreddit", "Enter the name of the subreddit: /r/")
            if not s:
                return
            if s.startswith('/r/'):
                s = s[len('/r/'):]
            self.grouping.add_subreddit(s)

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
        dirname = tkFileDialog.askdirectory()
        if dirname:
            self.settings.add_grouping(dirname)
        self.state.grouping = dirname

class GUIState(object):
    def __init__(self, grouping=None, subreddit=None):
        self.grouping = grouping
        self.subreddit = subreddit
    def tuple(self):
        return (self.grouping, self.subreddit)
