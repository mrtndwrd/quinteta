from mp3objects import *
import eyeD3
from mutagen.easyid3 import EasyID3
import os
import copy
# from collections import defaultdict -- Don't know where to place this :( now it is in mp3objects
class scan:
    """ 
    Class that walks through every directory in a given directory, finding MP3-files
    and saving their tags in artist, album and song objects.
    """
    # A tuple of songs
    songs = []
    # The current artist and album name, needed for automatically creating 
    # dictionary entries
    currentArtistName = ""
    currentAlbumName = ""
    # The dictionairies containing all the artists and albums
    albums = defaultdict()
    artists = defaultdict()
    def __init__(self):
        """
        When initializing, the albums and artists dictionaries are assigned 
        standard objects.
        """
        self.albums = defaultdict(lambda: album(copy.copy(self.currentAlbumName), copy.copy(self.currentArtistName)))
        self.artists = defaultdict(lambda: artist(copy.copy(self.currentArtistName)))
    def readall(self, directory):
        """
        Read all the mp3 files in a directory and its subdirectory
        """
        for direc in os.walk(directory):
            for file in direc[2]:
                # check if the file has .mp3 file extension
                if file.endswith(".mp3"):
                    try:
                        songEle = self.readmp3(direc[0] + "/" + file)
                    except ValueError:
                        songEle = song(direc[0] + "/" + file)
                        print "Could not parse " + direc[0] + "/" + file 
                        print "only saving fileName"
                    self.currentAlbumName = songEle.properties['album'][0] 
                    self.currentArtistName = songEle.properties['artist'][0]
                    currentSong = copy.copy(songEle)
                    self.songs.append(currentSong)
                    self.albums[self.currentAlbumName].addSong(songEle)
                    self.artists[self.currentArtistName].albums[self.currentAlbumName] = self.albums[self.currentAlbumName]
        return self.songs
    def readmp3(self, fileName):
        """
        Read some mp3file with file name fileName
        """
        tag = EasyID3(fileName)
        keys = ['artist', 'album', 'title']
        songElement = song(fileName)
        for key in keys:
            try:
                songElement.setKey(key, tag[key])
            except KeyError:
                songElement.setKey(key, "Unknown")
        return songElement
     def save(self, libraryName="library"):
        """
        Save the current knowledge to a file to library.maf (maf files: Maartens
        Awesome Fyletype) or any provided library name.
        """
        f = file(libraryName, 'write')
        for ar in a.artists:
            write("Artist:")
            write(a.artists[ar].artistName)
            write("Album:")
            for al in a.artists[ar].albums:
                write( a.artists[ar].albums[al].albumName)
                write("songs:")
                for s in a.artists[ar].albums[al].songs:
                    write(s.fileName)

a = scan()
songs = a.readall("/home/maarten/Music/")
for ar in a.artists:
    print "Artist:"
    print a.artists[ar].artistName
    print "Album:"
    for al in a.artists[ar].albums:
        print a.artists[ar].albums[al].albumName
        print "songs:"
        for s in a.artists[ar].albums[al].songs:
            print s.fileName
