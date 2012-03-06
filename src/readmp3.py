from mp3objects import *
import eyeD3
from mutagen.easyid3 import EasyID3
import os
import copy
import codecs
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
                        songEle = self.readmp3(unicode(direc[0] + "/" + file, 'utf-8'))
                    except ValueError:
                        songEle = song(unicode(direc[0] + "/" + file, 'utf-8'))
                        print "Could not parse " + direc[0] + "/" + file 
                        print "only saving fileName"
                    self.currentAlbumName = songEle.properties['album'][0] 
                    self.currentArtistName = songEle.properties['artist'][0]
                    currentSong = copy.copy(songEle)
                    self.songs.append(currentSong)
                    self.albums[self.currentAlbumName].addSong(songEle)
                    self.artists[self.currentArtistName].addSong(self.currentAlbumName, songEle)
        return self.songs
    def readmp3(self, fileName):
        """
        Read some mp3file with file name fileName
        """
        tag = EasyID3(fileName)
        keys = ['artist', 'album']
        songElement = song(fileName)
        try:
            songElement.setKey('title', tag['title'][0])
        except KeyError:
            tag['title'] = 'Unknown'
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
        f = codecs.open(libraryName + '.maf', 'w', 'utf-8-sig')
        for ar in self.artists:
            f.write("Artist:\n")
            f.write(self.artists[ar].artistName + "\n")
            for al in self.artists[ar].albums:
                f.write("Album:\n")
                f.write( self.artists[ar].albums[al].albumName + "\n")
                f.write("Songs:\n")
                for s in self.artists[ar].albums[al].songs:
                    f.write(s.fileName + "\n")
                    f.write(s.properties['title'] + '\n')
        f.close()
    def load(self, libraryName='library.maf'):
        f = codecs.open(libraryName, 'r', 'utf-8')

        for line in f:
            if line == 'Songs:\n':
                line = f.readline()
                while True:
                    # For some reason this cannot be called in the while:
                    songEle = song(line[0:-1], self.currentArtistName, self.currentAlbumName, f.readline()[0:-1])
                    currentSong = copy.copy(songEle)
                    self.songs.append(currentSong)
                    self.albums[self.currentAlbumName].addSong(songEle)
                    self.artists[self.currentArtistName].albums[self.currentAlbumName] = self.albums[self.currentAlbumName]
                    line = f.readline()
                    if line == 'Artist:\n' or line == u'' or line == 'Album:\n':
                        break
            if line == 'Artist:\n':
                # Remove the \n by taking [0:-1]
                self.currentArtistName = f.readline()[0:-1]
            elif line == 'Album:\n':
                self.currentAlbumName = f.readline()[0:-1]
        f.close()

a = scan()
#songs = a.readall("/home/maarten/Music/")
#a.save()
a.load()
print a.songs[201].properties
