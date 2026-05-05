import json

CONFIG_PATH = "config/config.json"

def load_config():
    with open(CONFIG_PATH, "r") as file:
        return json.load(file)