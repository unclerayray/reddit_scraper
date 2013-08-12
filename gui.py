# gui.py

import Tkinter

import settings
import scrape
import itertools
                
class ScraperWindow(object):
    def __init__(self):
        self.root = self.get_root()
        self.settings = settings.Settings()
        self.add_elements()
        self.add_listeners()
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

    def add_elements(self):
        root = self.root

        ## Subreddit command pane.
        command_frame = Tkinter.Frame(root)
        command_buttons = [("Scrape", self.scrape, 0, 0),
                           ("Load", self.load, 0, 1),
                           ("Save", self.save, 0, 2),
                           ("Add", self.add_subreddit, 1, 1),
                           ("Remove", self.remove_subreddit, 1, 2)]
        
        for text, command, row, col in command_buttons:
            Tkinter.Button(command_frame, text=text, command=command).grid(row=row, column=col)

        self.entry_field = Tkinter.Entry(command_frame)
        self.entry_field.grid(row=1, column=0)

        command_frame.grid(row=0, column=2)

        ## Subreddit listbox.
        self.listbox = Tkinter.Listbox(root)
        self.listbox.grid(row=0, column=3)
        self.listbox.insert(Tkinter.END, "<Subreddits>")

        ## Directory command pane.
        directory_frame = Tkinter.Frame(root)
        directory_buttons = [("Add Directory", self.add_directory, 0, 0)]
        for text, command, row, col in directory_buttons:
            Tkinter.Button(directory_frame, text=text, command=command).grid(row=row, column=col)

        directory_frame.grid(row=0, column=0)

        ## Directory listbox.
        self.directory_listbox = Tkinter.Listbox(root)
        self.directory_listbox.grid(row=0, column=1)
        self.directory_listbox.insert(Tkinter.END, "<Directories>")
        
    def add_listeners(self):
        pass
        # bind some things

    def update_gui(self):
        pass

    def remove_sr_placeholder(self):
        for i in xrange(self.listbox.size()):
            if self.listbox.get(i) == "<Subreddits>":
                index = i
                break
        else:
            return
        self.listbox.delete(index)

        
    def add_subreddit(self):
        self.remove_sr_placeholder()
        text = self.entry_field.get()
        self.listbox.insert(Tkinter.END, text)

    def remove_subreddit(self):
        pass

    def save(self):
        pass

    def load(self):
        self.settings.load()
        self.update_gui()
    
    def add_directory(self):
        pass
        
    def scrape(self):
        scrape.scrape(self.settings)
