"""(Incomplete) Tests for Song class."""
from song import Song

def run_tests():
   """test empty song (defaults)"""
   song = Song()
   print(song)
   assert song.artist == ""
   assert song.title == ""
   assert song.year == 0


# test initial-value song
   song2 = Song("My Happiness", "Powderfinger", 1996, True)
   print(song2)
   assert song2.is_required
# TODO: write tests to show this initialisation works

# test mark_learned()
   song2.mark_learned()
   print(song2)
   assert song2.is_required

run_tests()
# TODO: write tests to show the mark_learned() method works