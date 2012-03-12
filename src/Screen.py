import tkMessageBox
from Tkinter import *
import readmp3
from collections import defaultdict

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, library, root
    library = Tk()
    library.title('Library')
    library.geometry('471x228+1987+257')
    lib = readmp3.Scan()
    lib.load()
    w_win = Library (lib, library)
    init()
    library.mainloop()
def create_Library (root):
    '''Starting point when module is imported by another program.'''
    global library, w_win
    #if library: # So we have only one instance of window.
    #    return
    library = Toplevel (root)
    library.title('Library')
    library.geometry('471x228+1987+257')
    lib = readmp3.Scan()
    lib.load()
    print 'bladibla'
    print lib.artists[0]
    w_win = Library (lib, library)
    init()
    return w_win
def destroy_Library ():
    global library
    library.destroy()
    library = None
def init():
    pass



class Library:
    lib = readmp3.Scan()
    artists = defaultdict()
    albums = defaultdict()
    songs = defaultdict()

    def printinfo(self):
        print "text"
        return

    def __init__(self, lib, master=None):
        # Set background of toplevel window to match
        # current style
        self.master = master
        """
        style = ttk.Style()
        theme = style.theme_use()
        default = style.lookup(theme, 'background')
        self.master.configure(background=default)
        """
        
        #awesomeButton = Button(self.master, text='Awesomeness', command=self.printinfo)
        #awesomeButton.grid(row=0, column=0)
        # Make a listbox for all the artist, to be able to click one
        self.artistFrame = self.makeListFrame(self.master, lib.artists)
        self.artistFrame.grid(row=0, column=0)
        self.albumFrame = self.makeListFrame(self.master, lib.albums)
        self.albumFrame.grid(row=0, column=1)
        self.songFrame = self.makeListFrame(self.master, lib.songs)
        self.songFrame.grid(row=0, column=2)

    def makeListFrame(self, master, input):
        currentFrame = Frame(master)
        scrollbar = Scrollbar(currentFrame, orient=VERTICAL)
        currentList = Listbox(currentFrame, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        currentList.pack(side=LEFT, fill=BOTH, expand=1)
        scrollbar.config(command=currentList.yview)
        if isinstance(input, defaultdict):
            for item in sorted(input):
                currentList.insert(END, item)
        else:
            for item in sorted(input):
                currentList.insert(END, item.properties['title'])
        return currentFrame
        #items = map(int, list.curselection())

        """
        Label(self.master, text="Naam:").grid(row=0)
        self.entryNaam = Entry(self.master)
        self.entryNaam.grid(row=0, column=1, columnspan=3)
        
        Label(self.master, text="Geslacht").grid(row=1)
        self.g = StringVar()
        self.Frame1 = Frame(self.master)
        self.Frame1.grid(row=1, column=1)
        entryGeslachtM = Radiobutton(self.Frame1, text="Man", variable=self.g, value="m")
        entryGeslachtV = Radiobutton(self.Frame1, text="Vrouw", variable=self.g, value="v")
        entryGeslachtM.grid(row=1, column=1)
        entryGeslachtV.grid(row=1, column=2)
        
        Label(self.master, text="Rol").grid(row=2)
        self.r = StringVar()
        self.Frame2 = Frame(self.master)
        self.Frame2.grid(row=2, column=1)
        entryRolP = Radiobutton(self.Frame2, text="Prins", variable=self.r, value="prins")
        entryRolK = Radiobutton(self.Frame2, text="Kind", variable=self.r, value="kind")
        entryRolW = Radiobutton(self.Frame2, text="Bakker", variable=self.r, value="winkelier")

        entryRolP.grid(row=2, column=1)
        entryRolK.grid(row=2, column=2)
        entryRolW.grid(row=2, column=3)

        Label(self.master, text="Instrument:").grid(row=3)
        self.entryInstrument = Entry(self.master)
        self.entryInstrument.grid(row = 3, column = 1, columnspan = 3)
             
        self.Button1 = Button (self.master, text="OK", command=self.printinfo)
        self.Button1.grid(row=4, column=2)
        """





if __name__ == '__main__':
    vp_start_gui()
