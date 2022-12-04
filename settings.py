import json

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
