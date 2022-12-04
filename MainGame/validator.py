from collections import OrderedDict

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

            if len(number_range) > 1:
                if value >= min_val and value <= max_val:
                    break
                else:
                    print(f"\n[ERROR]: Enter a number between {min_val}-{max_val}!")
                    continue
            else:
                print(f"\n[ERROR]: Enter valid number to use this option!")
        return value

    def show_errors(self):
        print()
        for number in self.error_numbers:
            if number != 0:
                print(f"[ERROR]: {self.error_list[number]}")
        self.error_numbers.clear()
    
