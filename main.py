import os
import constants as c

from validator import Validator
from engine import Engine
from game import Game

clear = lambda: os.system("cls" if os.name == "nt" else "clear")

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