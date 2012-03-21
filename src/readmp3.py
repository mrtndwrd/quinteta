from mp3objects import *
import eyeD3
from mutagen.easyid3 import EasyID3
import os
import copy
import codecs
# from collections import defaultdict -- Don't know where to place this :( now it is in mp3objects
class Scan:
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
                    self.currentAlbumName = songEle.properties['album']
                    self.currentArtistName = songEle.properties['artist']
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
        keys = ['artist', 'album', 'tracknumber', 'title']
        songElement = song(fileName)
        #try:
        #    songElement.setKey('title', tag['title'][0])
        #except KeyError:
        #    tag['title'] = 'Unknown'
        for key in keys:
            try:
                songElement.setKey(key, tag[key][0])
            except KeyError:
                songElement.setKey(key, "Unknown")
        return songElement
    def save(self, libraryName="library"):
        """
        Save the current knowledge to a file to library.maf (maf files: Maartens
        Awesome Filetype) or any provided library name.
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
                    f.write("keys:\n")
                    for key in s.properties:
                        if key != 'artist' and key != 'album':
                            f.write(key + "," +  unicode(s.properties[key]) + '\n')
                    f.write("endKeys\n")
        f.close()
    def load(self, libraryName='library.maf'):
        f = codecs.open(libraryName, 'r', 'utf-8')

        for line in f:
            if line == 'Songs:\n':
                line = f.readline()
                while True:
                    # For some reason this cannot be called in the while:
                    songEle = song(line[0:-1], self.currentArtistName, self.currentAlbumName)
                    if(f.readline() == 'keys:\n'):
                        while True:
                            line = f.readline()
                            if(line == 'endKeys\n'):
                                break
                            line = line.split(',')
                            tag = line[0]
                            value = ''.join(line[1:])[0:-1]
                            songEle.setKey(tag, value)
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

if __name__ == '__main__':
    a = Scan()
    songs = a.readall("/media/VIRUS/music/")
    a.save()
    #a.load()
    print "boobies"
    #s.Library.printinfo()
