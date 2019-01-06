
# create your Song class in this file

class Song:
    def __init__(self, title="", artist="", year=0, is_required=""):
        """Determine items a song would help"""
        self.artist = artist
        self.title = title
        self.year = year
        self.is_required = is_required

    def __str__(self):
        """Display an announcement when a song is inpputed"""
        if self.is_required == "n":
            is_required = "learned"
            return ("You have learned {} by {} ({})".format(self.title,self.artist, self.year))
        else:
            is_required = "y"
            return ("You have not learned {} by {} ({})".format(self.title,self.artist, self.year))

    def mark_learned(self):
        """Mark the song learned"""
        self.is_required = 'n'
        return self.is_required

