from collections import defaultdict
class song: 
    """
    Object containing the important information of an mp3 file
    """
    properties = defaultdict()
    fileName = ""
    def __init__(self, fileNameIn, artist="Unknown", album="Unknown", title="Unknown"):
        self.fileName = fileNameIn
        self.properties = defaultdict()
        self.properties['artist'] = artist
        self.properties['album'] = album
        self.properties['title'] = title
        self.properties['tracknumber'] = 0

    def setKey(self, key, value):
        self.properties[key] = value

    def __cmp__(self, other):
        ownTrackNumber = int(self.properties['tracknumber'].split('/')[0])
        otherTrackNumber = int(other.properties['tracknumber'].split('/')[0])
        if ownTrackNumber < otherTrackNumber:
            return -1
        elif ownTrackNumber > otherTrackNumber:
            return 1
        else:
            return 0

class album:
    """
    Object containing the import information of an album
    """
    properties = defaultdict()
    albumName = ""
    songs = []
    def __init__(self, albumName, artist="Unknown"):
        self.properties = defaultdict()
        self.albumName = albumName
        self.songs = []

    def addSong(self, song):
        self.songs.append(song)

class artist:
    """
    Object containing the import information of an album
    """
    artistName = ""
    properties = defaultdict()
    albums = defaultdict()
    lastAddedAlbum = ""
    def __init__(self, artistName):
        self.artistName = artistName
        self.properties = defaultdict()
        self.albums = defaultdict(lambda: album(self.lastAddedAlbum, self.artistName))
    def setArtist(self, artistName):
        self.artistName = artistName
    def addSong(self, albumName, song):
        self.lastAddedAlbum = albumName
        self.albums[albumName].addSong(song)

