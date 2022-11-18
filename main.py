from genericpath import isfile
import random
import json
import os

import constants as c

from enum import Enum
from collections import OrderedDict

clear = lambda: os.system("cls" if os.name == "nt" else "clear")

class Level(Enum):
    EASY_MODE = 0
    NORMAL_MODE = 1
    HARD_MODE = 2

class Words:
    def __init__(self):
        self.engine_word = None

    def generate_word(self, mode):
        file = ""
        if mode == Level.EASY_MODE.value:
            file = c.EASY_MODE
        elif mode == Level.NORMAL_MODE.value:
            file = c.NORMAL_MODE
        else:
            file = c.HARD_MODE

        try:
            with open(file) as f:
                data = f.read().split(' ')
                self.engine_word = random.choice(data)
        except FileNotFoundError:
            print(f"[ERROR]: File {file} not found")
            exit()

class Validator:
    error_list = {
        1: "Word must contain only unique letters!",
        2: "Your word is too long!",
        3: "Your word is too short!",
    }
    error_numbers = []

    def isUnique(self, word):
        unique_word = "".join(OrderedDict.fromkeys(word)) 
        if word == unique_word:
            return True
        else:
            self.error_numbers.append(1)
            return False
    
    def isLengthEqual(self, player_word, engine_word):
        player_word_length = len(player_word)
        engine_word_length = len(engine_word)

        if player_word_length == engine_word_length:
            return True
        elif player_word_length > engine_word_length:
            self.error_numbers.append(2)
            return False
        else:
            self.error_numbers.append(3)
            return False

    @staticmethod
    def get_integer_input(prompt, *number_range):
        min_val = number_range[0]
        max_val = number_range[1]
        while True:
            try:
                value = int(input(prompt))
            except ValueError:
                print("\n[ERROR]: Try again!")
                continue

            if value >= min_val and value <= max_val:
                break
            elif min_val != value:
                print(f"\n[ERROR]: Enter a {min_val} number to go back!")
            else:
                print(f"\n[ERROR]: Enter a number between {min_val}-{max_val}!")
                continue
        return value

    def show_errors(self):
        print()
        for number in self.error_numbers:
            if number != 0:
                print(f"[ERROR]: {self.error_list[number]}")
        self.error_numbers.clear()
    

class Settings:
    def __init__(self):
        hints, tries, level = self.get_config()
        self.settings_hints = hints
        self.settings_tries = tries
        self.settings_level = level

    def get_config(self):
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                config_keys = []
                for key in config.keys():
                    config_keys.append(config[key])
                return config_keys
        except FileNotFoundError:
            print(f"[ERROR]: Config file not found!")
            exit()
    
    def update_config(self):
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)

            config["hints"] = self.settings_hints
            config["tries"] = self.settings_tries
            config["level"] = self.settings_level

            with open("config.json", "w") as config_file:
                json.dump(config, config_file, indent=4)

        except FileNotFoundError:
            print(f"[ERROR]: Config file not found!")
            exit()

class Stats:
    def __init__(self, bulls = 0, cows = 0):
        self.settings = Settings()
        self.tries = self.settings.settings_tries
        self.bulls = bulls
        self.cows = cows

    def show_stats(self):
        print(f"[SCORE]: {self.bulls} Bulls, {self.cows} Cows. You have {self.tries} tries left!")
    
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
            "Do you want to save your score?\n\n"
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
                f.write(f"Guessed: {word} - [{len(word)} letter word] [{mode} mode] [{self.tries} tries left] [max {self.settings.settings_tries} tries]\n")
            if os.path.isfile(file_name):
                print(f"\nYour score has been successfully saved to {file_name}!")

class Player:
    def __init__(self):
        self.stats = Stats()
        self.name = os.getlogin()
        self.player_word = None

    def player_input(self):
        self.player_word = input("\nInsert a word: ")

class Engine:
    def __init__(self):
        self.player = Player()
        self.words = Words()

    def score_logic(self, player_word, engine_word, hint):
        bulls = 0
        cows = 0
        i = 0

        print("\nGuess the word: ", end=" ")
        for letter in engine_word:
            char = " "
            if player_word.count(letter) and letter != player_word[i]:
                cows += 1
            if letter == player_word[i]:
                if hint:
                    char = letter

                bulls += 1
            print(f"[{char}]", end=" ")

            i += 1

        print()
        print()
        self.player.stats.update_stats(bulls, cows)

    def initial_message(self, word):
        mode = self.show_mode()
        print(f"\n[MODE]: {mode}\n\nHello, {self.player.name}! You have {self.player.stats.settings.settings_tries} tries, use them carefully. Good luck & have fun!\n")
        print("Generated word contains:", end=" ")
        for i in word:
            print("[ ]", end=" ")
        print(f"- {len(word)} letters")
    
    def determine_end(self):
        # here
        if self.player.stats.tries == 0 and self.player.stats.bulls != len(self.words.engine_word):
            print("[LOSE]: No more tries! Better luck next time!\n")
            return True
        elif self.player.stats.bulls == len(self.words.engine_word):
            print("[WIN]: Congratz, you rock!\n")
            self.player.stats.export_stats(self.words.engine_word)
            return True
        else:
            return False
    
    def show_mode(self):
        if self.player.stats.settings.settings_level == Level.EASY_MODE.value:
            return "Easy"
        elif self.player.stats.settings.settings_level == Level.NORMAL_MODE.value:
            return "Normal"
        else:
            return "Hard"

class Game:
    def __init__(self, x):
        game_run = True
        while game_run:
            clear()
            x.words.generate_word(x.player.stats.settings.settings_level)
            engine_word = x.words.engine_word
            print(f"[TEST] {engine_word}") # helper
            x.initial_message(engine_word)
            play = True
            
            while play:
                x.player.player_input()
                player_word = x.player.player_word
                x.player.stats.tries -= 1

                validate = Validator()

                if validate.isUnique(player_word) and validate.isLengthEqual(player_word, engine_word):
                    x.score_logic(player_word, engine_word, x.player.stats.settings.settings_hints)
                else:
                    validate.show_errors()

                x.player.stats.show_stats()
                play = not x.determine_end()

                x.player.stats.reset_stats()

            continuing = Validator.get_integer_input(
                "\nDo you want to continue?\n\n[1] Yes\n[2] No\n\nYour choice: ",
                1,
                2
            )

            x.player.stats.reset_tries()

            if continuing == 1:
                continue
            else:
                game_run = False

class Menu:
    def __init__(self):
        self.host = Engine()
        self.menu_functions = {
            1: [self.new_game_menu, "New Game"],
            2: [self.rules_menu, "Rules"],
            3: [self.settings_menu, "Settings"],
            0: [self.quit_game, "Quit Game"]
        }
        self.menu_run = True
        while self.menu_run:
            clear()
            print("\n[ MENU ]\n")
            for key in self.menu_functions.keys():
                print(f"[{key}] {self.menu_functions[key][1]}")
            
            user_input = Validator.get_integer_input("\nYour choice: ", 0, 3)
            self.menu_functions[user_input][0]()

    def new_game_menu(self):
        clear()
        Game(self.host)

    def rules_menu(self):
        clear()
        run = True
        while run:
            print(f"\n[ GAME RULES ]\n{c.RULES}")
            user_input = Validator.get_integer_input(
                "\n[0] Go back\n\nYour choice: ",
                0,
                0
            )
            if user_input == 0:
                run = False
    
    def settings_menu(self):
        clear()
        SettingsMenu(self.host)

    def quit_game(self):
        self.menu_run = False
        print("\nBye, bye!")

class SettingsMenu:
    def __init__(self, obj): 
        self.obj = obj
        self.settings_run = True

        while self.settings_run:
            clear()
            print("\n[ SETTINGS ]\n")
            self.settings_functions = {
                1: [self.hint_setting, f"Toggle Hints - {self.obj.player.stats.settings.settings_hints}"],
                2: [self.tries_setting, f"Change number of tries - {self.obj.player.stats.settings.settings_tries}"],
                3: [self.mode_setting, f"Change game difficulty - {self.obj.player.stats.settings.settings_level}"],
                0: [self.go_back, "Go back"]
            }
            for key in self.settings_functions.keys():
                print(f"[{key}] {self.settings_functions[key][1]}")
            
            user_input = Validator.get_integer_input("\nChoose setting: ", 0, 3)
            self.settings_functions[user_input][0]()

    def hint_setting(self):
        print()
        self.obj.player.stats.settings.settings_hints = not self.obj.player.stats.settings.settings_hints
        if self.obj.player.stats.settings.settings_hints:
            print("[SETTINGS]: Hints enabled")
        else:
            print("[SETTINGS]: Hints disabled")
        
        self.obj.player.stats.settings.update_config()

    def tries_setting(self):
        print()
        tries = Validator.get_integer_input(
            "Enter maximum tries: ",
            1,
            100
        )
        self.obj.player.stats.tries = tries
        self.obj.player.stats.settings.settings_tries = tries
        self.obj.player.stats.settings.update_config()
        
    def mode_setting(self):
        print()
        clear()
        self.obj.player.stats.settings.settings_level = Validator.get_integer_input(
            "[0] Normal (3-4 letters)\n"
            "[1] Medium (5-9 letters)\n"
            "[2] Hard (+10 letters)\n\nNew difficulty: ",
            0,
            2
        )
        self.obj.player.stats.settings.update_config()

    def go_back(self):
        self.settings_run = False

if __name__ == "__main__":
    Menu()