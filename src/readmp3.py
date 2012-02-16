import eyeD3
from song import song

class scan:
    """ 
    Class that can read an mp3 file's tags using ffmpeg (for now let's focus 
    on artist, album, track number and track name)
    """
    def readmp3(self, fileName):
        """
        read some mp3file
        """
        tag = eyeD3.Tag()
        tag.link(fileName)
        return song(tag.getArtist(), tag.getAlbum(), tag.getTitle())


a = scan()
mp3 = a.readmp3("/media/VIRUS/music/Supertramp/Supertramp - Very Best/01 School.mp3")
print mp3.title
    

