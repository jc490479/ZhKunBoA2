"""
Name:ZhuKunBo
Date:January 5,2019
Brief Project Description:This program is create the GUI that display songlist.Users can add songs in songlist，sort songlist by year,
 artist,title and can clear what they input.
GitHub URL:https://github.com/JCUS-CP1404/a2--jc490479
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from song import Song
from songlist import SongList
from kivy.properties import StringProperty
from kivy.properties import ListProperty

class SongsToLearnApp(App):
    """ Main program:Display a list of songs in a GUI model using Kivy app"""
    message = StringProperty()        # Define status text
    news = StringProperty()
    current_sort = StringProperty()   # Define sort
    sort_choices = ListProperty()

    def __init__(self, **kwargs):
        """Construct main app"""
        super(SongsToLearnApp, self).__init__(**kwargs)
        self.song_list = SongList()
        self.sort_choices = ["title", "artist", "year", "is_required"]
        self.current_sort = self.sort_choices[0]
        self.song_list.load_songs()

    def build(self):
        """
        Build the Kivy GUI.
        :return: reference to the root Kivy widgit
        """
        self.title = "Songs to learn by ZhuKunBo"          # Name GUI name
        self.root = Builder.load_file('app.kv')    # Load app.kivy
        self.create_widget()                      # Create widget in GUI
        return self.root

    def change_sort(self, sorting_choice):
        """
        Function to change the sorting of the song list
        :param sorting_choice: Based on what choice the user selects, the song list will be sorted that way
        :return: sorted song list
        """
        self.message = "song have been sorted by: {}".format(sorting_choice)
        self.song_list.sort(sorting_choice)
        self.root.ids.entriesBox.clear_widgets()
        self.create_widget()
        sort_index = self.sort_choices.index(sorting_choice)
        self.current_sort = self.sort_choices[sort_index]

    def Clear_input(self):
        """Clear inputs after clicking the Clear button"""
        self.root.ids.song_title.text = ''     # Clear input
        self.root.ids.song_artist.text = ''
        self.root.ids.song_year.text = ''

    def create_widget(self):
        """Create widgets that lists the songs from the csv file"""
        self.root.ids.entriesBox.clear_widgets()
        num_song = len(self.song_list.list_songs)  # Determine the number of songs in the list
        learned_song = 0
        for song in self.song_list.list_songs:  # Loop from first song to last song
            title = song.title
            artist = song.artist
            year = song.year
            learned = song.is_required
            display_text = self.generateDisplayText(title, artist, year,
                                                    learned)  # Display song's information on the widget
            if learned == "n":
                learned_song += 1
                button_color = self.getColor(learned)
            else:
                button_color = self.getColor(learned)

            temp_button = Button(text=display_text, id=song.title,
                                 background_color=button_color)  # Mark the song learned
            temp_button.bind(on_release=self.press_entry)  # Display message of the GUI status
            self.root.ids.entriesBox.add_widget(temp_button)
        self.message = "To learn: {}. Learned: {}".format(num_song - learned_song,
                                                          learned_song)  # Display number of song learned or not learned

    def generateDisplayText(self, title, artist, year, learned):
        """Formating text display in the message"""
        if learned == "n":
            display_text = "{} by {} ({}) (Learned)".format(title, artist, year)
        else:
            display_text = "{} by {} ({})".format(title, artist, year)

        return display_text

    def getColor(self, learned):
        """Display colors of the song learned and not learned"""
        if learned == "n":
            button_color = [0.4, 0.6, 0, 1]
        else:
            button_color = [0.4, 0.7, 0.9, 1]
        return button_color

    def press_entry(self, button):
        """Display the 2nd message"""
        buttonText = button.text
        selectedSong = Song()
        for song in self.song_list.list_songs:
            songDisplayText = self.generateDisplayText(song.title, song.artist, song.year, song.is_required)
            if buttonText == songDisplayText:
                selectedSong = song
                break

        selectedSong.mark_learned()   # Mark the song learned
        self.root.ids.entriesBox.clear_widgets()  # Apply to GUI
        self.create_widget()

        self.news = "You have learned {}".format(selectedSong.title)  # Display change in news

    def add_songs(self):
        """
        Add the new song
        :return: Add the song inputted to the song list
        """
        if self.root.ids.song_title.text == "" or self.root.ids.song_artist.text == "" or self.root.ids.song_year.text == "":
            self.root.ids.status2.text = "All fields must be completed"
            return
        try:
            # Define song item inputted
            song_title = str(self.root.ids.song_title.text)
            song_artist = str(self.root.ids.song_artist.text)
            song_year = int(self.root.ids.song_year.text)
            is_required = "y"

            # Add songs's input to the songlist
            self.song_list.add_to_list(song_title, song_artist, song_year, is_required)
            temp_button = Button(
                text=self.generateDisplayText(song_title, song_artist, song_year, is_required))
            temp_button.bind(on_release=self.press_entry)

            # Format new song item
            temp_button.background_color = self.getColor(is_required)
            self.root.ids.entriesBox.add_widget(temp_button)
            self.create_widget()

            # Clear input after adding song
            self.root.ids.song_title.text = ""
            self.root.ids.song_artist.text = " "
            self.root.ids.song_year.text = ""

        except ValueError:  # Display error when type is wrong
            self.news = "Please enter a valid year"

    def on_stop(self):  # Stop GUI and save
        self.song_list.save_songs()

# Run the SongsToLearnApp
SongsToLearnApp().run()
