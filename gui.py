# gui.py

import Tkinter
import scrape

class ScrapeWindow(object):
    def __init__(self):
        self.root = Tkinter.Tk()
        self.add_elements(self.root)
        self.add_listeners(self.root)
        self.root.mainloop()
        
    def add_elements(self, root):
        pass
        # add some buttons and whatnot
        # file opener dialogue...
        
    def add_listeners(self, root):
        pass
        # bind some things
        
    def scrape(self):
        scrape.do_some_scraping(settings)
        # This shouldn't all be contained in main() anymore, in scrape.py
    
