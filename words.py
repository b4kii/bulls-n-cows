import random
from level import Level
import constants as c

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
