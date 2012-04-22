# Needed to call audacious:
import os
# Needed to make interfaces:
from Tkinter import *
import tkFileDialog
# Not sure if needed:
#import tkMessageBox
# Needed to read everything to memory:
import readmp3
import mp3objects
# Needed by readmp3:
from collections import defaultdict

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, library, root
    library = Tk()
    library.title('Library')
    #library.wm_iconbitmap('icon.ico')
    library.iconbitmap("@icon.xbm")
    #library.geometry('471x228+1987+257')
    lib = readmp3.Scan()
    lib.load()
    w_win = Library (lib, library)
    init()
    library.mainloop()
def create_Library (root, lib=None):
    '''Starting point when module is imported by another program.'''
    global library, w_win
    #if library: # So we have only one instance of window.
    #    return
    if(root == None):
        library = Tk()
    else:
        library = Toplevel (root)
    library.title('Library')
    library.iconbitmap("@icon.xbm")
    #library.geometry('471x228+1987+257')
    if(lib == None):
        lib = readmp3.Scan()
        lib.load()
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
    """ A class that starts a Library window """
    lib = readmp3.Scan()

    def printinfo(self, selected, tiep):
        """ This is a test case that should not be taken seriously """
        #print self.lib.artists[selected.widget.get(5)].artistName
        if tiep=='tiep':
            print self.lib.artists[selected.widget.get(map(int, selected.widget.curselection())[0])].artistName
        #print selected.widget.get(map(int, selected.widget.curselection())[0])
        #print selected.widget.curselection()
        #print map(int, selected.widget.curselection())
        return

    # For some reason the trace gives useless arguments...
    # Don't use the varibles!
    def find(self, type=None, nothing=None, pythonVar=None):
        artistContent = defaultdict()
        for item in self.artistFrame.input:
            if self.artistFrame.input[item].artistName.lower().find(self.findEntry.get().lower()) >= 0:
                artistContent[item] = self.artistFrame.input[item]
        self.artistFrame.setContent(artistContent)
        albumContent = defaultdict()
        for item in self.albumFrame.input:
            if self.albumFrame.input[item].albumName.lower().find(self.findEntry.get().lower()) >= 0:
                albumContent[item] = self.albumFrame.input[item]
        self.albumFrame.setContent(albumContent)
        songContent = []
        for item in self.songFrame.input:
            if item.properties['title'].lower().find(self.findEntry.get().lower()) >= 0:
                songContent.append(item)
        self.songFrame.setContent(songContent)

    def clear(self):
        self.findString.set('')

    def __init__(self, lib, master=None):
        """ Init needs a lib to start on. This is a Scan() object from 
        readmp3.py, containing the library 
        """
        self.master = master
        self.lib = lib
        # This will be the frame for adding a new library
        self.libraryFrame = Frame(master)
        self.libraryFrame.pack()
        self.libDirectoryLabel = Label(self.libraryFrame)
        self.libDirectoryLabel['text'] = 'Library directory: '
        self.libDirectoryLabel.pack(side=LEFT)
        self.libDirectoryEntry = Entry(self.libraryFrame)
        self.libDirectoryEntry.pack(fill=X, side=LEFT)
        self.libDirectoryButton = Button(self.libraryFrame, text="Browse", command=self.browseLibrary)
        self.libDirectoryButton.pack(side=LEFT)
        self.libScanButton = Button(self.libraryFrame, text='Scan Directory', command=self.scanLibrary)
        self.libScanButton.pack(side=LEFT)
        self.libSaveButton = Button(self.libraryFrame, text='Save Library', command=self.saveLibrary)
        self.libSaveButton.pack(side=LEFT)
        # A search box is needed: (according to SOME people)
        self.findFrame = Frame(master)
        self.findFrame.pack()
        # This will be the frame containing all the listFrames
        self.listFramesFrame = Frame(master)
        self.listFramesFrame.pack(fill=BOTH, expand=True)
        # Make a listbox for all the artist, to be able to click one
        self.songFrame = ListFrame(self.listFramesFrame, None, self.lib.songs, 'songs')
        self.songFrame.frame.pack(fill=BOTH, side=RIGHT)
        self.albumFrame = ListFrame(self.listFramesFrame, self.songFrame, self.lib.albums, 'albums')
        self.albumFrame.frame.pack(fill=BOTH, side=RIGHT)
        self.artistFrame = ListFrame(self.listFramesFrame, self.albumFrame, self.lib.artists, 'artists')
        self.artistFrame.frame.pack(fill=BOTH, side=RIGHT)
        self.buttonFrame = Frame(master)
        self.buttonFrame.pack(fill=BOTH)
        self.afterButton = Button(self.buttonFrame, text='Enqueue after', command=self.enqueueAfter)
        self.afterButton.pack(side=RIGHT)
        self.insteadButton = Button(self.buttonFrame, text='Enqueue instead', command=self.enqueueInstead)
        self.insteadButton.pack(side=RIGHT)
        self.findString = StringVar()
        self.findString.trace('w', self.find)
        self.findEntry = Entry(self.buttonFrame, textvariable=self.findString)
        self.findEntry.pack(fill=X, side=RIGHT)
        self.findLabel= Label(self.buttonFrame, text='Find: ')
        self.findLabel.pack(side=RIGHT)
        self.findClearButton = Button(self.buttonFrame, text='Clear', command=self.clear)
        self.findClearButton.pack(side=RIGHT)
        self.songFrame.bind("<Double-Button-1>", self.enqueueAfter)
        self.artistFrame.bind("<Double-Button-1>", self.enqueueAfter)
        self.albumFrame.bind("<Double-Button-1>", self.enqueueAfter)

    def browseLibrary(self):
        """ Opens a browser window to select the current Library directory """
        options = {}
        options['mustexist'] = True
        options['parent'] = self.master
        options['title'] = 'Choose library directory'
        self.libDirectoryEntry.insert(0, tkFileDialog.askdirectory(**options))
        print self.libDirectoryEntry.get()

    def saveLibrary(self):
        """ Saves the current library to library.maf """
        self.lib.save()
        pass

    def scanLibrary(self):
        """ Scans the directory selected in the entry box """
        # TODO: Remove this print statement after testing phase is over
        print 'scanning ' +  self.libDirectoryEntry.get()
        self.lib = readmp3.Scan()
        self.lib.readall(self.libDirectoryEntry.get())
        destroy_Library()
        create_Library(None, self.lib)

    def enqueueAfter(self, uselessargument=None):
        self.enqueue('after')

    def enqueueInstead(self):
        self.enqueue('instead')


    def enqueue(self, afterOrInstead):
        """ Enqueues a or more file(s) after the current playlist """
        if self.songFrame.currentList.curselection() != ():
            # Enqueue only this song.
            cmd = u'audacious2 ' 
            if afterOrInstead == 'after':
                cmd += '-e "'
            else:
                cmd += '-E "'
            # cmd += unicode(sorted(currentAlbum.songs)[map(int, self.songFrame.currentList.curselection())[0]].fileName + '" &')
            cmd += unicode(self.songFrame.currentContent[map(int, self.songFrame.currentList.curselection())[0]].fileName + '" &')
            print cmd
            # System call has to be encoded, because of unicode characters like u'\xe6'
            os.system(cmd.encode('utf-8'))
        elif self.albumFrame.currentList.curselection() != ():
            # there is a selected album
            currentAlbum = self.albumFrame.currentContent[self.albumFrame.currentList.get(map(int, self.albumFrame.currentList.curselection())[0])]
            # enqueue the entire album
            self.enqueueAlbum(currentAlbum, afterOrInstead)
        elif self.artistFrame.currentList.curselection() != ():
            # Queue all the albums in this artist
            currentArtist = self.artistFrame.input[self.artistFrame.currentList.get(map(int, self.artistFrame.currentList.curselection())[0])]
            for album in currentArtist.albums:
                self.enqueueAlbum(currentArtist.albums[album], afterOrInstead)

    def enqueueAlbum(self, album, afterOrInstead):
        cmd = 'audacious2 '
        if afterOrInstead == 'after':
            cmd += '-e '
        else:
            cmd += '-E '
        for track in sorted(album.songs):
            cmd += '"' + track.fileName + '" '
        # Make a new console branch:
        cmd += '&'
        # System call has to be encoded, because of unicode characters like u'\xe6'
        os.system(cmd.encode('utf-8'))


class ListFrame:
    """ A class making a frame with interesting information """

    def __init__(self, master, subFrame, input, tiep):
        self.tiep = tiep
        self.input = input
        self.frame = Frame(master)
        self.frame.pack(fill=BOTH, expand=1)
        self.subFrame = subFrame
        # Variable that holds the objects currently in the list
        self.currentContent = input

        scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.currentList = Listbox(self.frame, yscrollcommand=scrollbar.set, exportselection=0, selectmode=EXTENDED)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.currentList.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.currentList.yview)
        if isinstance(input, defaultdict):
            for item in sorted(input):
                self.currentList.insert(END, item)
        else:
            for item in input:
                self.currentList.insert(END, "%s. %s" % (item.properties['tracknumber'], item.properties['title']))
        self.currentList.bind("<<ListboxSelect>>", self.callback)

    def callback(self, selected):
        if self.tiep == 'artists':
            self.subFrame.setContent(self.input[selected.widget.get(map(int, selected.widget.curselection())[0])].albums)
        elif self.tiep == 'albums':
            self.subFrame.setContent(sorted(self.input[selected.widget.get(map(int, selected.widget.curselection())[0])].songs))

    def setContent(self, content):
        self.currentList.delete(0, END)
        if isinstance(content, defaultdict):
            for item in sorted(content):
                self.currentList.insert(END, item)
        else:
            self.currentContent = content
            for item in content:
                self.currentList.insert(END, "%s. %s" % (item.properties['tracknumber'], item.properties['title']))

    def bind(self, event, call):
        self.currentList.bind(event, call)
        

if __name__ == '__main__':
    vp_start_gui()
