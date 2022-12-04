import os

from settings import Settings
from validator import Validator
from level import Level

class Stats:
    def __init__(self, bulls = 0, cows = 0):
        self.settings = Settings()
        self.tries = self.settings.settings_tries
        self.bulls = bulls
        self.cows = cows

    def show_stats(self, player_word, engine_word, hint):
        if len(player_word) == len(engine_word):
            print("\nGuess the word: ", end=" ")
            i = 0
            for letter in engine_word:
                char = " "
                if letter == player_word[i]:
                    if hint:
                        char = letter

                print(f"[{char}]", end=" ")

                i += 1

        print(f"\n[SCORE]: {self.bulls} Bulls, {self.cows} Cows. You have {self.tries} tries left!")
    
    def reset_stats(self):
        self.bulls = 0
        self.cows = 0

    def reset_tries(self):
        print(f"Tries: {self.settings.settings_tries}")
        self.tries = self.settings.settings_tries

    def update_stats(self, bulls = 0, cows = 0):
        self.bulls += bulls
        self.cows += cows
    
    def export_stats(self, word):
        user_input = Validator().get_integer_input(
            "\nDo you want to save your score?\n\n"
            "[1] Yes\n"
            "[2] No\n\n"
            "Your choice: ",
            1,
            2
        )
        mode = ""
        if self.settings.settings_level == Level.EASY_MODE.value:
            mode = "Easy"
        elif self.settings.settings_level == Level.NORMAL_MODE.value:
            mode = "Normal"
        else:
            mode = "Hard"

        if user_input == 1:
            file_name = "highscores.txt"
            with open(file_name, "a") as f:
                f.write(f"Guessed: {word} - [{len(word)} letter word] [mode: {mode}] [tries left: {self.tries}] [max tries: {self.settings.settings_tries}] [hints: {self.settings.settings_hints}]\n")
            if os.path.isfile(file_name):
                print(f"\n[Your score has been successfully saved to {file_name}!]")
