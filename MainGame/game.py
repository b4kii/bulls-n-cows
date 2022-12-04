import os

from MainGame.validator import Validator

clear = lambda: os.system("cls" if os.name == "nt" else "clear")

class Game:
    def __init__(self, x):
        game_run = True
        while game_run:
            clear()
            x.words.generate_word(x.player.stats.settings.settings_level)
            engine_word = x.words.engine_word
            print(f"[DEBUG] {engine_word}") # helper, to delete
            x.initial_message(engine_word)
            play = True
            
            while play:
                x.player.player_input()
                player_word = x.player.player_word
                x.player.stats.tries -= 1

                validate = Validator()

                if validate.isUnique(player_word) and validate.isLengthEqual(player_word, engine_word):
                    x.score_logic(player_word, engine_word)
                else:
                    validate.show_errors()

                x.player.stats.show_stats(player_word, engine_word, x.player.stats.settings.settings_hints)
                play = not x.determine_end()

                x.player.stats.reset_stats()

            continuing = Validator.get_integer_input(
                "\nDo you want to continue?\n\n[1] Yes\n[2] No\n\nYour choice: ",
                1,
                2
            )

            x.player.stats.reset_tries()

            if continuing == 2:
                game_run = False
