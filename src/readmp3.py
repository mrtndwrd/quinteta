import eyeD3
from mutagen.easyid3 import EasyID3
import os
import copy
from mp3objects import *

class scan:
    """ 
    Class that can read an mp3 file's tags using ffmpeg (for now let's focus 
    on artist, album, track number and track name)
    """
    songs = []
    currentArtistName = ""
    currentAlbumName = ""
    albums = defaultdict()
    artists = defaultdict()
    def __init__():
        albums = defaultDict(lambda: album(self.currentAlbumName, self.currentArtistName))
        artists = defaultdict(lambda: artist(self.currentArtistName))
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
                        self.currentAlbumName = songEle.properties['album'] 
                        self.currentArtistName = songEle.properties['artist']
                        self.songs.append(copy.copy(songEle))
                        self.albums.append(copy.copy(album(songEle.albumName)))
                    except ValueError:
                        print "Could not parse " + direc[0] + "/" + file 
                        print "only saving fileName"
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

a = scan()
songs = a.readall("/home/maarten/Music/")
for s in songs:
   print s.properties['title']
