import os

from stats import Stats

class Player:
    def __init__(self):
        self.stats = Stats()
        self.name = os.getlogin()
        self.player_word = None

    def player_input(self):
        self.player_word = input("\nInsert a word: ")
