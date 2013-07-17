# gui.py

import Tkinter
import scrape

class ScraperWindow(object):
    def __init__(self):
        self.root = self.get_root()
        self.settings = self.get_saved_settings()
        self.add_elements()
        self.add_listeners()
        self.root.after(100, self.center_window)
        self.root.mainloop()
        
    def center_window(self):
        w = float(self.root.winfo_screenwidth())
        h = float(self.root.winfo_screenheight())
        rootsize = tuple(int(i) for i in self.root.geometry().split('+')[0].split('x'))
        x = w/2 - rootsize[0]/2
        y = h/2 - rootsize[1]/2
        self.root.geometry("%dx%d+%d+%d" % (rootsize + (x, y)))

    def get_saved_settings(self):
        return eval(open('settings.txt', 'r').read())

    def get_root(self):
        return Tkinter.Tk()
        
    def add_elements(self):
        root = self.root
        command_frame = Tkinter.Frame(root)
        scrape_button = Tkinter.Button(command_frame, text="Scrape", command=self.scrape)
        scrape_button.pack()
        command_frame.pack()

        scrollbar = Tkinter.Scrollbar(root)
        scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)

        listbox = Tkinter.Listbox(root)
        listbox.pack()

        for i in range(100):
            listbox.insert(Tkinter.END, i)


        # add some buttons and whatnot
        # file opener dialogue...
        
    def add_listeners(self):
        pass
        # bind some things
        
    def scrape(self):
        scrape.scrape(self.settings)
        # This shouldn't all be contained in main() anymore, in scrape.py
    
