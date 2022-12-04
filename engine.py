from player import Player
from words import Words
from level import Level

class Engine:
    def __init__(self):
        self.player = Player()
        self.words = Words()

    def score_logic(self, player_word, engine_word):
        bulls = 0
        cows = 0
        i = 0
        for letter in engine_word:
            if player_word.count(letter) and letter != player_word[i]:
                cows += 1
            if letter == player_word[i]:
                bulls += 1
            i += 1
        self.player.stats.update_stats(bulls, cows)

    def initial_message(self, word):
        mode = self.show_mode()
        print(f"\n[MODE]: {mode}\n\nHello, {self.player.name}! You have {self.player.stats.settings.settings_tries} tries, use them carefully. Good luck & have fun!\n")
        print("Generated word contains:", end=" ")
        for i in word:
            print("[ ]", end=" ")
        print(f"- {len(word)} letters")
    
    def determine_end(self):
        if self.player.stats.tries == 0 and self.player.stats.bulls != len(self.words.engine_word):
            print("[LOSE]: No more tries! Better luck next time!")
            return True
        elif self.player.stats.bulls == len(self.words.engine_word):
            print("[WIN]: Congratz, you rock!")
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
